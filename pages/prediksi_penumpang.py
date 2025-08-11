import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

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
st.title("📈 Prediksi Jumlah Penumpang")

# Progress bar
progress = st.progress(50)
st.markdown("### Langkah 2 dari 4: Prediksi Penumpang")

# Cek apakah semua data sudah ada di session_state DAN bukan None
if st.session_state.get("data_penumpang") is None:
    st.error("❌ Data penumpang belum diupload")
    if st.button("⬅️ Kembali ke Input Data"):
        st.switch_page("pages/input_data.py")
    st.stop()
    
if st.session_state.get("data_libur") is None:
    st.error("❌ Data hari libur belum diupload")
    if st.button("⬅️ Kembali ke Input Data"):
        st.switch_page("pages/input_data.py")
    st.stop()

if (
    st.session_state.get("data_penumpang") is not None and
    st.session_state.get("data_libur") is not None 
):
    # Semua data tersedia → lanjut
    df_penumpang = st.session_state["data_penumpang"]
    df_libur = st.session_state["data_libur"]
    # Semua data aman → lanjut
    # df_penumpang = st.session_state["data_penumpang"]
    # df_libur = st.session_state["data_libur"]
    # armada_total = st.session_state["armada_total"]
    # armada_per_jam = st.session_state["armada_per_jam"]

    st.success("Data lengkap.")
    st.write("Cuplikan data penumpang:")
    st.dataframe(df_penumpang.head())

    # if "data_penumpang" in st.session_state:
    #     st.write("Data Penumpang:")
    #     st.dataframe(st.session_state["data_penumpang"])
    # else:
    #     st.warning("❌ Data penumpang belum tersedia.")

    # if "data_libur" in st.session_state:
    #     st.write("Data Libur:")
    #     st.dataframe(st.session_state["data_libur"])
    # else:
    #     st.warning("❌ Data libur belum tersedia.")

    # if "armada_total" in st.session_state:
    #     st.write(f"Jumlah Armada Total: {st.session_state['armada_total']}")
    # else:
    #     st.warning("❌ Armada total belum tersedia.")

    # if "armada_per_jam" in st.session_state:
    #     st.write(f"Jumlah Armada per Jam: {st.session_state['armada_per_jam']}")
    # else:
    #     st.warning("❌ Armada per jam belum tersedia.")

    # Ambil data dari session_state
   

   # === Preprocessing ===
    df_penumpang['tanggal'] = pd.to_datetime(df_penumpang['tanggal'])
    le_hari = LabelEncoder()
    le_rute = LabelEncoder()

    df_penumpang['hari_encoded'] = le_hari.fit_transform(df_penumpang['hari'])
    df_penumpang['rute_encoded'] = le_rute.fit_transform(df_penumpang['rute'])
    df_penumpang['liburnasional'] = df_penumpang['libur nasional'].astype(bool).astype(int)

    X = df_penumpang[['hari_encoded', 'libur nasional', 'rute_encoded', 'jam']]
    y = df_penumpang['jumlah penumpang']

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Prediksi untuk besok
    besok = df_penumpang['tanggal'].max() + timedelta(days=1)
    hari_besok = besok.strftime("%A")
    is_weekend = hari_besok in ["Saturday", "Sunday"]
    libur_list = pd.to_datetime(df_libur["tanggal libur"], format="%d/%m/%Y")
    is_libur = pd.to_datetime(besok.date()) in libur_list

    rute_list = df_penumpang['rute'].unique()
    jam_list = list(range(5, 23))

    data_prediksi = []
    for rute in rute_list:
        for jam in jam_list:
            data_prediksi.append([
                le_hari.transform([hari_besok])[0],
                int(is_libur),
                le_rute.transform([rute])[0],
                jam
            ])

    prediksi = model.predict(data_prediksi)
    
    data_prediksi = pd.DataFrame(data_prediksi, columns=['Hari_encoded', 'Libur Nasional', 'Rute_encoded', 'Jam'])
    
    data_hasil_prediksi = pd.DataFrame({
    'Tanggal': [besok.date()] * len(data_prediksi),
    'Hari': [hari_besok] * len(data_prediksi),
    'Rute': le_rute.inverse_transform(data_prediksi['Rute_encoded']),
    'Jam': data_prediksi['Jam'],
    'Jumlah Penumpang Prediksi': prediksi.astype(int)
   })
    # Susun hasil
    # hasil_df = pd.DataFrame(data_prediksi, columns=['Hari_encoded', 'Libur Nasional', 'Rute_encoded', 'Jam'])
    # hasil_df['Tanggal'] = besok.date()
    # hasil_df['Hari'] = hari_besok
    # hasil_df['Rute'] = le_rute.inverse_transform(hasil_df['Rute_encoded'])
    # hasil_df['JumlahPenumpang_Prediksi'] = prediksi.astype(int)
    # hasil_df = pd.DataFrame()


    # Tampilkan
    st.subheader("Hasil Prediksi Jumlah Penumpang Besok")
    st.dataframe(data_hasil_prediksi)

    # Download sebagai CSV
    hasil_csv = data_hasil_prediksi.to_csv(index=False)
    st.download_button(
    label="📥 Download CSV Hasil Prediksi",
    data = hasil_csv.encode('utf-8'),
    file_name='hasil_prediksi.csv',
    mime='text/csv'
    )
    st.session_state["hasil_prediksi"] = data_hasil_prediksi
    if st.session_state.get("hasil_prediksi") is not None:
        st.success("📁 File prediksi_penumpang_besok.csv telah disimpan.")
        
        # Tombol untuk lanjut ke pembagian armada
        col1, col2 = st.columns([7,3])
        with col2:
            if st.button("⏩ Lanjut ke Pembagian Armada", use_container_width=True):
                st.switch_page("pages/pembagian_armada.py")
else:
    st.warning("⚠️ Data belum lengkap.")
