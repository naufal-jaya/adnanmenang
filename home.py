import streamlit as st
from utils import load_css, div

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Prediksi Penumpang Bus", 
    page_icon="🚍", 
    layout="wide",
    menu_items={},
    initial_sidebar_state="collapsed"
)

st.markdown(
    div(
        "<h1>Prediksi Penumpang Bus</h1>",
        class_name="header"
    ),
    unsafe_allow_html=True
)

st.subheader("Aplikasi ini berfungsi untuk:")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Prediksi Penumpang")
    st.markdown("Prediksi penumpang berdasarkan data historis dan hari libur menggunakan model machine learning.")

with col2:
    st.markdown("### Pembagian Armada")
    st.markdown("Pembagian armada berdasarkan pembobotan penumpang untuk mengoptimalkan penggunaan armada bus.")


st.markdown("---")

# Tombol untuk memulai
if st.button("Mulai Input Data", use_container_width=True):
    st.switch_page("pages/input_data.py")