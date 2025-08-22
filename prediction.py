import streamlit as st
import pandas as pd
import plotly.express as px
import gdown
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

def tampilkan_prediction():
    st.title("Prediksi Produk Terjual dalam N Tahun")

    # --- Download dataset ---
    file_id = "1UqzmIBfHeQBwbCA1Y4P9YOtuQB2orgBH"
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "data.csv"
    gdown.download(url, output, quiet=False)
    df = pd.read_csv(output)

    # --- Konversi tanggal ---
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['sold_at'] = pd.to_datetime(df['sold_at'], errors='coerce')  # unsold = NaT

    # --- Sidebar filter ---
    st.sidebar.header("Filter Options")
    brand_options = df['product_brand'].unique()
    brand_filter = st.sidebar.multiselect("Select Product Brand:", options=brand_options, default=brand_options)

    category_options = df['product_category'].unique()
    category_filter = st.sidebar.multiselect("Select Product Category:", options=category_options, default=category_options)

    min_date = df['created_at'].min().date()
    max_date = df['created_at'].max().date()
    date_range = st.sidebar.date_input("Select Created Date Range:", [min_date, max_date], min_value=min_date, max_value=max_date)

    # --- Slider prediksi tahun ---
    years_range = st.sidebar.slider(
        "Prediksi Produk Terjual dalam Berapa Tahun?",
        min_value=1,
        max_value=10,
        value=5,
        step=1
    )

    # --- Apply filter ---
    filtered_df = df[
        (df['product_brand'].isin(brand_filter)) &
        (df['product_category'].isin(category_filter)) &
        (df['created_at'].dt.date >= date_range[0]) &
        (df['created_at'].dt.date <= date_range[1])
    ]

    if filtered_df.empty:
        st.warning("Tidak ada data setelah filter. Silakan periksa filter Anda.")
        return

    # --- Buat target dinamis ---
    filtered_df['sold_within_Ny'] = filtered_df.apply(
        lambda row: 1 if pd.notnull(row['sold_at']) and (row['sold_at'] - row['created_at']).days <= years_range*365 else 0,
        axis=1
    )

    # --- Fitur & target ---
    features = ['product_id','cost','product_category','product_brand','product_retail_price','product_department','product_distribution_center_id']
    X = filtered_df[features]
    y = filtered_df['sold_within_Ny']

    # --- Preprocessing + Model ---
    numeric_features = ['cost','product_retail_price']
    categorical_features = ['product_id','product_category','product_brand','product_department','product_distribution_center_id']

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

    rf_pipe = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced'))
    ])

    # --- Fit model ---
    rf_pipe.fit(X, y)

    # --- Prediksi probabilitas aman ---
    proba = rf_pipe.predict_proba(X)
    if proba.shape[1] == 1:
        filtered_df['pred_proba_Ny'] = proba[:,0]
        st.warning("Data setelah filter hanya memiliki satu kelas target. Semua probabilitas sama.")
    else:
        filtered_df['pred_proba_Ny'] = proba[:,1]

    # --- Tampilkan top 10 produk ---
    top_pred = filtered_df.sort_values('pred_proba_Ny', ascending=False).head(10)
    st.subheader(f"Top 10 Produk dengan Probabilitas Terjual dalam {years_range} Tahun Tertinggi")
    st.dataframe(top_pred[['product_name','product_brand','product_category','created_at','pred_proba_Ny']].round(2))

    # --- Plot interaktif ---
    fig = px.bar(
        top_pred,
        x='product_name',
        y='pred_proba_Ny',
        text=top_pred['pred_proba_Ny'].round(2),
        color='product_brand',
        title=f"Top 10 Produk dengan Probabilitas Terjual dalam {years_range} Tahun",
        labels={'pred_proba_Ny':f'Probabilitas Terjual {years_range} Tahun', 'product_name':'Product Name'}
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        margin=dict(t=50,b=80,l=50,r=20),
        height=500
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)