# import streamlit as st
# import pandas as pd
# import time

# with open("style.css") as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# if  st.button("Home", key="btn_home", use_container_width=False):
#     st.switch_page("home.py")

# st.markdown('<div class="custom-btn-group">', unsafe_allow_html=True)

# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     if st.button("Input Data", key="btn_input", use_container_width=True):
#         st.switch_page("pages/input_data.py")

# with col2:
#     if st.button("Prediksi Penumpang", key="btn_prediksi", use_container_width=True):
#         st.switch_page("pages/prediksi_penumpang.py")

# with col3:
#     if st.button("Pembagian Armada", key="btn_armada", use_container_width=True):
#         st.switch_page("pages/pembagian_armada.py")

# with col4:
#     if st.button("Penjadwalan Armada", key="btn_jadwal", use_container_width=True):
#         st.switch_page("pages/penjadwalan.py")

# st.markdown('</div>', unsafe_allow_html=True)

# st.title("🚍 Pembagian Jumlah Armada")


# progress_container = st.empty()

# for percent in range(75):
#     track_color = "#C6D3D4"  # warna track
#     fill_color = "#89c2c6"   # warna progress
#     progress_container.markdown(f"""
#         <div style="
#             background-color: {track_color};
#             border-radius: 4px;
#             height: 10px;
#             width: 100%;
#             overflow: hidden;
#         ">
#             <div style="
#                 background-color: {fill_color};
#                 height: 100%;
#                 width: {percent}%;
#                 transition: width 0.1s;
#             "></div>
#         </div>
#     """, unsafe_allow_html=True)
#     time.sleep(0.02)

# # Cek hasil prediksi tersedia
# if st.session_state.get("hasil_prediksi") is None:
#     st.error("❌ Hasil prediksi belum tersedia")
#     if st.button("Kembali ke Input Data", use_container_width=True):
#         st.switch_page("pages/input_data.py")
#     st.stop()

# # Armada total
# armada_total_input = st.text_input("Jumlah armada total", value="")
# armada_total = int(armada_total_input) if armada_total_input.isdigit() else None

# # Armada per jam
# armada_per_jam_input = st.text_input("Jumlah armada per jam per rute", value="")
# armada_per_jam = int(armada_per_jam_input) if armada_per_jam_input.isdigit() else None

# # Validasi
# if (
#     armada_total is not None and 
#     armada_total >= 1 and
#     armada_per_jam is not None and 
#     armada_per_jam >= 1
# ):

#     df = st.session_state["hasil_prediksi"]

#     df.columns = df.columns.str.strip().str.lower()

#     # Pastikan data valid
#     required_cols = {"tanggal", "hari", "rute", "jam", "jumlah penumpang prediksi"}
#     if not required_cols.issubset(df.columns):
#         st.error(f"CSV harus mengandung kolom: {required_cols}")
#         st.stop()

#     # Agregasi per tgl, rute, jam
#     df_grouped = df.groupby(["tanggal", "rute", "jam"], as_index=False).sum()
#     df_grouped["bobot"] = df_grouped["jumlah penumpang prediksi"] / df_grouped["jumlah penumpang prediksi"].sum()

#     # Alokasi awal
#     df_grouped["armada_dialokasikan"] = df_grouped["bobot"] * armada_total
#     df_grouped["armada_dialokasikan"] = df_grouped["armada_dialokasikan"].apply(
#         lambda x: max(armada_per_jam, int(round(x)))
#     )

#     # Koreksi jika melebihi armada_total
#     total_allocated = df_grouped["armada_dialokasikan"].sum()
#     selisih = total_allocated - armada_total

#     if selisih > 0:
#         df_grouped = df_grouped.sort_values("jumlah penumpang prediksi")
#         for idx in df_grouped.index:
#             if selisih <= 0:
#                 break
#             if df_grouped.at[idx, "armada_dialokasikan"] > armada_per_jam:
#                 df_grouped.at[idx, "armada_dialokasikan"] -= 1
#                 selisih -= 1

#     # Gabungkan hasil ke dataframe awal
#     df_hasil = pd.merge(df, df_grouped[["tanggal", "hari", "rute", "jam", "jumlah penumpang prediksi", "armada_dialokasikan"]],
#                         on=["tanggal", "rute", "jam"], how="left")
    
#     if df_hasil is not None:
#         st.success("Pembagian armada berhasil dilakukan.")
        
#         st.session_state["hasil_pembagian_armada"] = df_hasil
        
#         st.subheader("📊 Hasil Pembagian Armada")
#         st.dataframe(df_hasil)

#         # Tombol download
#         csv = df_hasil.to_csv(index=False).encode("utf-8")
#         col1, col2 = st.columns([7.3,2.7])
#         with col1:
#             st.download_button("📥 Download CSV", csv, file_name="hasil_pembagian_armada.csv", mime="text/csv")
#         with col2:
#             if st.button("Next - Penjadwalan", use_container_width=True):
#                 st.switch_page("pages/penjadwalan.py")



# else: st.write("Masukkan angka minimal 1 di kedua kolom.")    
import streamlit as st
import pandas as pd
import time
import numpy as np


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


st.title("🚍 Pembagian Jumlah Armada")


progress_container = st.empty()

for percent in range(75):
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

if st.session_state.get("hasil_prediksi") is None:
    st.error("❌ Hasil prediksi belum tersedia")
    if st.button("Kembali ke Input Data", use_container_width=True):
        st.switch_page("pages/input_data.py")
    st.stop()



df = st.session_state["hasil_prediksi"]

df.columns = df.columns.str.strip().str.lower()

# Pastikan data valid
required_cols = {"tanggal", "hari", "rute", "jam", "jumlah penumpang prediksi"}
if not required_cols.issubset(df.columns):
    st.error(f"CSV harus mengandung kolom: {required_cols}")
    st.stop()

# Armada total
armada_total_input = st.text_input("Jumlah armada total", value="")
armada_total = int(armada_total_input) if armada_total_input.isdigit() else None

# Armada per jam
armada_per_jam_input = st.text_input("Jumlah armada minimal yang beroperasi di tiap rute", value="")
armada_per_jam = int(armada_per_jam_input) if armada_per_jam_input.isdigit() else None

if (
    armada_total is not None and 
    armada_total >= 1 and
    armada_per_jam is not None and 
    armada_per_jam >= 1
    ):
    # Agregasi per tgl, rute, jam
    df_grouped = df.groupby(["tanggal", "rute", "jam"], as_index=False).sum()

    # Bobot per JAM (bukan global): proporsi penumpang rute terhadap total penumpang di jam tsb
    jam_total = df_grouped.groupby(["tanggal", "jam"])["jumlah penumpang prediksi"].transform("sum")
    df_grouped["bobot_jam"] = df_grouped["jumlah penumpang prediksi"] / jam_total.replace(0, 1)


    def alokasi_per_jam(group: pd.DataFrame):
        n = len(group)
        baseline = armada_per_jam * n
        alloc = np.zeros(n, dtype=int)
        warning_flag = False

        if armada_total >= baseline:
            # cukup untuk minimal
            base = np.full(n, armada_per_jam, dtype=int)
            remaining = armada_total - baseline

            alloc = base.copy()

            if remaining > 0:
                raw_extra = group["bobot_jam"].to_numpy() * remaining
                extra_floor = np.floor(raw_extra).astype(int)
                rem = remaining - extra_floor.sum()
                frac = raw_extra - extra_floor
                order = np.argsort(-frac)
                if rem > 0:
                    extra_floor[order[:rem]] += 1
                alloc += extra_floor

            # cek: kalau penumpang sedikit → cukup pakai minimal aja
            kapasitas_cukup = group["jumlah penumpang prediksi"].to_numpy() <= (armada_per_jam * 30)
            alloc[kapasitas_cukup] = armada_per_jam

        else:
            # tidak cukup untuk minimal → proporsional
            warning_flag = True
            raw = group["bobot_jam"].to_numpy() * armada_total
            alloc = np.floor(raw).astype(int)
            rem = armada_total - alloc.sum()
            if rem > 0:
                frac = raw - alloc
                order = np.argsort(-frac)
                alloc[order[:rem]] += 1

        group = group.copy()
        group["armada_dialokasikan"] = alloc
        group["warning_flag"] = warning_flag
        return group


    # Terapkan per (tanggal, jam)
    df_grouped = df_grouped.groupby(["tanggal", "jam"], group_keys=False).apply(alokasi_per_jam)

    # Gabungkan hasil
    df_hasil = pd.merge(
        df,
        df_grouped[["tanggal", "rute", "jam", "armada_dialokasikan"]],
        on=["tanggal", "rute", "jam"], how="left"
    )

    if df_hasil is not None:
        st.success("Pembagian armada berhasil dilakukan.")
        
        st.session_state["hasil_pembagian_armada"] = df_hasil
        
        st.subheader("📊 Hasil Pembagian Armada")
        st.dataframe(df_hasil)

        # Tombol download
        csv = df_hasil.to_csv(index=False).encode("utf-8")
        col1, col2 = st.columns([7.3,2.7])
        with col1:
            st.download_button("📥 Download CSV Pembagian Armada", csv, file_name="hasil_pembagian_armada.csv", mime="text/csv")
        with col2:
            if st.button("Next - Penjadwalan", use_container_width=True):
                st.switch_page("pages/penjadwalan.py")

    # Cek warning
    if df_grouped["warning_flag"].any():
        st.warning("⚠️ Armada total tidak cukup untuk memenuhi minimal di beberapa jam." \
        " Saran: jumlah armada total tidak kurang dari jumlah armada per jam dikali jumlah jam operasi.")

else: st.write("Masukkan angka minimal 1 di kedua kolom.")    
