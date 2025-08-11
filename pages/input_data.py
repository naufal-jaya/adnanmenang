# import streamlit as st
# import pandas as pd

# st.title("Prediksi Jumlah Penumpang dan Armada")

# # Upload file histori penumpang
# file_penumpang = st.file_uploader("Upload file CSV histori jumlah penumpang", type=["csv"])
# # Upload file libur nasional
# file_libur = st.file_uploader("Upload file CSV hari libur nasional", type=["csv"])

# # Input jumlah armada total dan per jam
# armada_total = st.number_input("Jumlah total armada yang dimiliki", min_value=1)
# armada_per_jam = st.number_input("Jumlah armada standar per jam per rute", min_value=1)

# # Jika semua input telah tersedia
# if file_penumpang and file_libur:
#     df_penumpang = pd.read_csv(file_penumpang)
#     df_libur = pd.read_csv(file_libur)

#     st.success("✅ File berhasil dimuat.")
#     st.subheader("Cuplikan Data Histori Penumpang")
#     st.dataframe(df_penumpang.head())

#     st.subheader("Cuplikan Data Hari Libur")
#     st.dataframe(df_libur.head())

#     if st.button("Lanjut"):
#      st.session_state["data_penumpang"] = df_penumpang
#      st.session_state["data_libur"] = df_libur
#      st.session_state["armada_total"] = armada_total
#      st.session_state["armada_per_jam"] = armada_per_jam
#      st.success("Data sudah siap! Silakan buka halaman prediksi untuk melanjutkan 🚀")

import streamlit as st
import pandas as pd

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Input Data", use_container_width=True):
        st.switch_page("pages/input_data.py")
with col2:
    if st.button("Prediksi Penumpang", use_container_width=True):
        st.switch_page("pages/prediksi_penumpang.py")
with col3:
    if st.button("Pembagian Armada", use_container_width=True):
        st.switch_page("pages/pembagian_armada.py")
with col4:
    if st.button("Penjadwalan Armada", use_container_width=True):
        st.switch_page("pages/penjadwalan.py")

st.title("🚀 Upload dan Simpan Data")

# Progress bar
progress = st.progress(25)
st.markdown("### Langkah 1 dari 4: Input Data")

# Menampilkan contoh file
st.subheader("📝 Contoh Format File CSV")
contoh_penumpang = pd.read_csv("pages/Contoh_Data_Penumpang.csv")
contoh_libur = pd.read_csv("pages/Contoh_Data_HariLibur.csv")

col1, col2 = st.columns(2)
with col1:
    st.write("Contoh Data Penumpang:")
    st.dataframe(contoh_penumpang.head())
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

st.markdown("---")

# 1. Upload file
input_penumpang = st.file_uploader("Upload CSV Penumpang", type=["csv"])
input_libur = st.file_uploader("Upload CSV Hari Libur", type=["csv"])

# 2. Input angka


# 3. Tombol lanjut
st.markdown("---")
if st.button("⏩ Lanjut ke Prediksi", use_container_width=True):
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
        st.error("❗ Upload kedua file sebelum lanjut.")





