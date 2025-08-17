import streamlit as st
import pandas as pd
import time

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if  st.button("Home", key="btn_home", use_container_width=False):
    st.switch_page("home.py")
    
st.markdown('<div class="custom-btn-group">', unsafe_allow_html=True)

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



progress_container = st.empty()

for percent in range(100):
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
                width: {percent + 1}%;
                transition: width 0.1s;
            "></div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(0.02)
st.title("Penjadwalan Armada")


if st.session_state.get("hasil_pembagian_armada") is not None:
    df_armada = st.session_state["hasil_pembagian_armada"]

    # Buat list untuk jadwal final
    jadwal_list = []

    for idx, row in df_armada.iterrows():
        # pastikan format datetime lengkap (tanggal + jam)
        tanggal = pd.to_datetime(row["tanggal"]).date()
        jam_awal = int(row["jam"])  
        jumlah_armada = int(row["armada_dialokasikan"])

        # total interval dibagi rata dalam 1 jam (misal 3 armada → jeda 60/3 = 20 menit)
        if jumlah_armada > 0:
            jeda_menit = 60 // jumlah_armada
        else:
            jeda_menit = 0

        # bikin datetime awal (gabungkan tanggal & jam_awal)
        start_datetime = pd.Timestamp(year=tanggal.year, month=tanggal.month, day=tanggal.day, hour=jam_awal)

        # loop setiap armada
        for i in range(jumlah_armada):
            waktu_berangkat = start_datetime + pd.Timedelta(minutes=i * jeda_menit)
            jadwal_list.append({
                "tanggal": tanggal,
                "rute": row["rute"],
                "armada_ke": i + 1,
                "waktu_berangkat": waktu_berangkat.strftime("%H:%M")
            })

    df_jadwal = pd.DataFrame(jadwal_list)

    st.subheader("📅 Jadwal Armada")
    st.dataframe(df_jadwal)

    st.button("Download Jadwal Armada", on_click=lambda: st.download_button)

    st.button("Kembali ke Home", use_container_width=True, on_click=lambda: st.switch_page("pages/home.py"))

else: 
    st.error("❌ Hasil pembagian armada belum tersedia")
    if st.button("Kembali ke Input Data", use_container_width=True):
        st.switch_page("pages/input_data.py")


