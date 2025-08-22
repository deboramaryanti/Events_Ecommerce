import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

def chart_2():
    st.title("Top Margin Brands Dashboard")

    file_id = "1UqzmIBfHeQBwbCA1Y4P9YOtuQB2orgBH"
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "IMFF_clean.csv"
    gdown.download(url, output, quiet=False)
    df = pd.read_csv(output)

    df['margin'] = df['product_retail_price'] - df['cost']

    st.sidebar.header("Filter Options")
    sold_options = df['sold_at'].unique()
    sold_filter = st.sidebar.multiselect("Select Sold Status:", options=sold_options, default=sold_options)

    brand_options = df['product_brand'].unique()
    brand_filter = st.sidebar.multiselect("Select Product Brand:", options=brand_options, default=brand_options)

    category_options = df['product_category'].unique()
    category_filter = st.sidebar.multiselect("Select Product Category:", options=category_options, default=category_options)

    min_date = df['created_at'].min().date()
    max_date = df['created_at'].max().date()
    date_range = st.sidebar.date_input("Select Created Date Range:", [min_date, max_date], min_value=min_date, max_value=max_date)

    filtered_df = df[
        (df['product_brand'].isin(brand_filter)) &
        (df['product_category'].isin(category_filter)) &
        (df['created_at'].dt.date >= date_range[0]) &
        (df['created_at'].dt.date <= date_range[1])
    ]

    brand_margin = (
        filtered_df.groupby('product_brand')['margin']
        .mean()
        .reset_index()
        .sort_values('margin', ascending=False)
        .head(10)  # ambil top 10
    )

    if not brand_margin.empty:
        top_margin_brand = brand_margin.iloc[0]
        st.write(f"**Brand dengan margin rata-rata tertinggi:** {top_margin_brand['product_brand']}")
        st.write(f"**Rata-rata margin:** {top_margin_brand['margin']:.2f}")

    fig = px.bar(
        brand_margin,
        x="product_brand",
        y="margin",
        text=brand_margin['margin'].round(2),
        title="Top 10 Brands by Average Margin",
        labels={"product_brand": "Product Brand", "margin": "Average Margin (USD)"}
    )

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
        marker_color='orange'
    )

    st.plotly_chart(fig, use_container_width=True)