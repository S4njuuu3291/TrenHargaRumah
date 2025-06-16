import streamlit as st
import joblib
import numpy as np
import pandas as pd

model = joblib.load(r'model\xgb_model_pipeline.pkl')

st.sidebar.title("Prediksi Harga Properti")
st.sidebar.info(
    "Input fitur properti lalu klik **Prediksi Harga**. "
    "Model berbasis XGBoost yang telah dilatih dengan data scraping listing online."
)

st.header("Input Fitur Properti")

list_lokasi = [
    "Medan Sunggal, Medan",
    "Medan Helvetia, Medan",
    "Medan Timur, Medan",
    "Medan Johor, Medan",
    "Medan Tembung, Medan",
    "Medan Barat, Medan",
    "Medan Kota, Medan",
    "Medan Selayang, Medan",
    "Medan Perjuangan, Medan",
    "Medan Area, Medan",
    "Medan Petisah, Medan",
    "Medan Polonia, Medan",
    "Medan Baru, Medan",
    "Medan Denai, Medan",
    "Medan Marelan, Medan",
    "Medan Maimun, Medan",
    "Medan Tuntungan, Medan",
    "Medan Amplas, Medan",
    "Medan Deli, Medan",
    "Medan Labuhan, Medan",
    "Medan Belawan, Medan",
]

list_tipe = ["Rumah", "Apartemen", "Ruko"]

col1, col2 = st.columns(2)
with col1:
    lokasi = st.selectbox("Lokasi (Kecamatan/Kota)", list_lokasi)
    tipe_properti = st.selectbox("Tipe Properti", list_tipe)
    jumlah_kamar_tidur = st.number_input(
        "Jumlah Kamar Tidur", min_value=0, max_value=20, value=2)
with col2:
    jumlah_kamar_mandi = st.number_input(
        "Jumlah Kamar Mandi", min_value=0, max_value=10, value=1)
    garasi = st.number_input(
        "Jumlah Garasi", min_value=0, max_value=5, value=1)
    luas_tanah = st.number_input(
        "Luas Tanah (m²)", min_value=10, max_value=1000, value=100)
    luas_bangunan = st.number_input(
        "Luas Bangunan (m²)", min_value=10, max_value=1000, value=80)

if st.button("Prediksi Harga"):
    input_df = pd.DataFrame({
        "lokasi": [lokasi],
        "jenis_properti": [tipe_properti],
        "jumlah_kamar_tidur": [jumlah_kamar_tidur],
        "jumlah_kamar_mandi": [jumlah_kamar_mandi],
        "garasi": [garasi],
        "luas_tanah": [luas_tanah],
        "luas_bangunan": [luas_bangunan]
    })
    pred_log = model.predict(input_df)[0]
    pred_price = np.expm1(pred_log)

    st.success(f"**Estimasi Harga Properti: Rp {pred_price:,.0f}**")

    st.caption(
        "_Note: Estimasi didapat dari model, hasil tidak selalu akurat untuk semua properti._")

st.markdown("---")
st.caption("© 2025 Sanjukin Pinem — XGBoost Properti Price Prediction Demo")
