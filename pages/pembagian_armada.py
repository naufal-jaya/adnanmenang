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

st.title("🚍 Pembagian Jumlah Armada")

# Progress bar
progress = st.progress(75)
st.markdown("### Langkah 3 dari 4: Pembagian Armada")

# Cek hasil prediksi tersedia
if st.session_state.get("hasil_prediksi") is None:
    st.error("❌ Hasil prediksi belum tersedia")
    if st.button("⬅️ Kembali ke Prediksi"):
        st.switch_page("pages/input_data.py")
    st.stop()
# armada_total = st.number_input("Jumlah armada total", min_value=1)
# armada_per_jam = st.number_input("Jumlah armada per jam per rute", min_value=1)

# Armada total
armada_total_input = st.text_input("Jumlah armada total", value="")
armada_total = int(armada_total_input) if armada_total_input.isdigit() else None

# Armada per jam
armada_per_jam_input = st.text_input("Jumlah armada per jam per rute", value="")
armada_per_jam = int(armada_per_jam_input) if armada_per_jam_input.isdigit() else None

# Validasi
if (
    armada_total is not None and 
    armada_total >= 1 and
    armada_per_jam is not None and 
    armada_per_jam >= 1
):


    df = st.session_state["hasil_prediksi"]

    df.columns = df.columns.str.strip().str.lower()

    # Pastikan data valid
    required_cols = {"tanggal", "hari", "rute", "jam", "jumlah penumpang prediksi"}
    if not required_cols.issubset(df.columns):
        st.error(f"CSV harus mengandung kolom: {required_cols}")
        st.stop()

    # Agregasi per tgl, rute, jam
    df_grouped = df.groupby(["tanggal", "rute", "jam"], as_index=False).sum()
    df_grouped["bobot"] = df_grouped["jumlah penumpang prediksi"] / df_grouped["jumlah penumpang prediksi"].sum()

    # Alokasi awal
    df_grouped["armada_dialokasikan"] = df_grouped["bobot"] * armada_total
    df_grouped["armada_dialokasikan"] = df_grouped["armada_dialokasikan"].apply(
        lambda x: max(armada_per_jam, int(round(x)))
    )

    # Koreksi jika melebihi armada_total
    total_allocated = df_grouped["armada_dialokasikan"].sum()
    selisih = total_allocated - armada_total

    if selisih > 0:
        df_grouped = df_grouped.sort_values("jumlah penumpang prediksi")
        for idx in df_grouped.index:
            if selisih <= 0:
                break
            if df_grouped.at[idx, "armada_dialokasikan"] > armada_per_jam:
                df_grouped.at[idx, "armada_dialokasikan"] -= 1
                selisih -= 1

    # Gabungkan hasil ke dataframe awal
    df_hasil = pd.merge(df, df_grouped[["tanggal", "hari", "rute", "jam", "jumlah penumpang prediksi", "armada_dialokasikan"]],
                        on=["tanggal", "rute", "jam"], how="left")
    
    if df_hasil is not None:
        st.success("Pembagian armada berhasil dilakukan.")
        
        st.session_state["hasil_pembagian_armada"] = df_hasil
        
        st.subheader("📊 Hasil Pembagian Armada")
        st.dataframe(df_hasil)

        # Tombol download
        csv = df_hasil.to_csv(index=False).encode("utf-8")
        col1, col2 = st.columns([7,3])
        with col1:
            st.download_button("📥 Download CSV", csv, file_name="hasil_pembagian_armada.csv", mime="text/csv")
        with col2:
            if st.button("Next - Penjadwalan", use_container_width=True):
                st.switch_page("pages/penjadwalan.py")



else: st.write("Masukkan angka minimal 1 di kedua kolom.")    

