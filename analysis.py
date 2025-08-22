import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def tampilkan_analysis():
    st.title("Product Analysis Dashboard")

    # Pilih jenis visualisasi
    pilihan_chart = st.radio("Pilih Chart:", [
        "Chart 1",
        "Chart 2"
    ])

    # --- CHART 1: Distribusi Produk ---
    if pilihan_chart.startswith("Chart 1"):
        import tren_chart
        tren_chart.chart_1()
    
    # --- CHART 2: Margin Produk ---
    elif pilihan_chart.startswith("Chart 2"):
        import margin
        margin.chart_2()