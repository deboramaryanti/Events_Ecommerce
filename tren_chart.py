import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

def chart_1():
    st.title("Top Selling Products Dashboard")
    
    file_id = "1UqzmIBfHeQBwbCA1Y4P9YOtuQB2orgBH"
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "data.csv"

    gdown.download(url, output, quiet=False)

    df = pd.read_csv(output)

    # --- Sidebar filter ---
    st.sidebar.header("Filter Options")
    sold_options = df['sold_at'].unique()
    sold_filter = st.sidebar.multiselect("Select Sold Status:", options=sold_options, default=sold_options)

    brand_options = df['product_brand'].unique()
    brand_filter = st.sidebar.multiselect("Select Product Brand:", options=brand_options, default=brand_options)

    category_options = df['product_category'].unique()
    category_filter = st.sidebar.multiselect("Select Product Category:", options=category_options, default=category_options)

    filtered_df = df[
        (df['product_brand'].isin(brand_filter)) &
        (df['product_category'].isin(category_filter))
    ]

    # --- Hitung jumlah produk terjual per brand ---
    brand_sales_count = (
        filtered_df[filtered_df['sold_at']=='sold']
        .groupby('product_brand')
        .size()
        .reset_index(name='sold_count')
        .sort_values('sold_count', ascending=False)
        .head(10)
    )

    # --- Buat grafik dengan Plotly Express ---
    fig = px.bar(
        brand_sales_count,
        x="product_brand",
        y="sold_count",
        text="sold_count",
        title="Top 10 Fast Moving Brands (by Sold Count)",
        labels={"product_brand": "Product Brand", "sold_count": "Sold Count"}
    )

    # --- Customisasi gaya mirip style transparan ---
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        margin=dict(t=50, b=40, l=50, r=20),
        height=500
    )

    fig.update_traces(
        textposition="outside",
        marker_color='skyblue'
    )

    # --- Tampilkan di Streamlit ---
    st.plotly_chart(fig, use_container_width=True)