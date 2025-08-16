
import streamlit as st
import pandas as pd
import pathlib
from utils import load_css
import time

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<div class="custom-btn-group">', unsafe_allow_html=True)

if  st.button("Home", key="btn_home", use_container_width=False):
    st.switch_page("home.py")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Input Data", key="btn_input", use_container_width=True):
        st.switch_page("pages/input_data.py")

with col2:
    if st.button("Prediksi Penumpang", key="btn_prediksi", use_container_width=True):
        st.switch_page("pages/prediksi_penumpang.py")

with col3:
    if st.button("Pembagian Armada", key="btn_armada", use_container_width=True):
        st.switch_page("pages/pembagian_armada.py")

with col4:
    if st.button("Penjadwalan Armada", key="btn_jadwal", use_container_width=True):
        st.switch_page("pages/penjadwalan.py")

st.markdown('</div>', unsafe_allow_html=True)

st.title("Unggah dan Simpan Data")

progress_container = st.empty()

for percent in range(25):
    track_color = "#C6D3D4"  # warna track
    fill_color = "#89c2c6"   # warna progress
    progress_container.markdown(f"""
        <div style="
            background-color: {track_color};
            border-radius: 4px;
            height: 10px;
            width: 100%;
            overflow: hidden;
        ">
            <div style="
                background-color: {fill_color};
                height: 100%;
                width: {percent}%;
                transition: width 0.1s;
            "></div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(0.02)

# Menampilkan contoh file
st.subheader("📝 Contoh Format File CSV")
contoh_penumpang = pd.read_csv("pages/Contoh_Data_Penumpang.csv")
contoh_libur = pd.read_csv("pages/Contoh_Data_HariLibur.csv")

col1, col2 = st.columns(2)
with col1:
    st.write("Contoh Data Penumpang:")
    st.dataframe(contoh_penumpang.head(), key ="contoh_penumpang")
    st.download_button(
        label="⬇️ Download Contoh Data Penumpang",
        data=contoh_penumpang.to_csv(index=False),
        file_name="Contoh_Data_Penumpang.csv",
        mime="text/csv"
    )

with col2:
    st.write("Contoh Data Hari Libur:")
    st.dataframe(contoh_libur)
    st.download_button(
        label="⬇️ Download Contoh Data Hari Libur",
        data=contoh_libur.to_csv(index=False),
        file_name="Contoh_Data_HariLibur.csv",
        mime="text/csv"
    )
st.write("Pastikan kolom file CSV yang diunggah sesuai dengan format contoh di atas.")
# st.markdown("<div class='markdown'>", unsafe_allow_html=True)
st.markdown("---")
# st.markdown("</div>", unsafe_allow_html=True)


# 1. Upload file
input_penumpang = st.file_uploader("Upload CSV Penumpang", type=["csv"])
input_libur = st.file_uploader("Upload CSV Hari Libur", type=["csv"])

st.button("🔄 Refresh", key="refresh_input", use_container_width=False)

# 2. Validasi input
st.markdown("---")

col1, col2 = st.columns([7,3])

error = None
with col2:
    if st.button("Next - Prediksi Penumpang", use_container_width=False):
        if input_penumpang and input_libur:
            df_penumpang = pd.read_csv(input_penumpang)
            df_libur = pd.read_csv(input_libur)

            df_penumpang.columns = df_penumpang.columns.str.strip().str.lower()

            required_cols_penumpang = {"hari", "libur nasional", "tanggal", "rute", "jam", "jumlah penumpang"}
            if not required_cols_penumpang.issubset(df_penumpang.columns):
                st.error(f"CSV penumpang harus mengandung kolom: Hari, Libur Nasional, Tanggal, Rute, Jam, Jumlah Penumpang")
                st.stop()
            
            df_libur.columns = df_libur.columns.str.strip().str.lower()

            required_cols_libur = {"tanggal libur", "hari libur"}
            if not required_cols_libur.issubset(df_libur.columns):
                st.error(f"CSV hari libur harus mengandung kolom: Tanggal Libur, Hari Libur")
                st.stop()
            
            st.session_state["data_penumpang"] = df_penumpang
            st.session_state["data_libur"] = df_libur
            st.session_state["csv_input_penumpang"] = input_penumpang
            st.session_state["csv_input_libur"] = input_libur

            st.success("✅ Data berhasil divalidasi!")
            st.switch_page("pages/prediksi_penumpang.py")
        else:
            error = True
        
if error:
    st.error("❗ Upload kedua file sebelum lanjut.")

else:
    pass




