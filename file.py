import os
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Konfigurasi Halaman (Judul & Layout Lebar)
st.set_page_config(
    page_title="Dashboard Aesthetic Pink", page_icon="𓍢ִ໋🌷͙֒✧", layout="wide"
)

# 2. CSS Custom untuk Judul Aesthetic Warna Pink & Tampilan Lainnya
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,400&family=Poppins:wght@300;400;600&display=swap');

    .aesthetic-title {
        font-family: 'Playfair Display', serif;
        color: #ff69b4; /* Warna Pink Hot/Aesthetic */
        font-size: 42px;
        font-weight: 600;
        text-align: left;
        margin-bottom: 0px;
        text-shadow: 1px 1px 2px rgba(255, 105, 180, 0.2);
    }
    
    .subtitle {
        font-family: 'Poppins', sans-serif;
        color: #888888;
        font-size: 15px;
        margin-bottom: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Menampilkan Judul Aesthetic
st.markdown('<p class="aesthetic-title">✨ PDS Dashboard ✨</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Eksplorasi data keuangan dan daerah dengan sentuhan manis 🌸</p>',
    unsafe_allow_html=True,
)


# 3. Load Data secara Aman
@st.cache_data
def load_data():
  dir_path = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(dir_path, "data.csv")
  return pd.read_csv(file_path)


try:
  df = load_data()
except Exception as e:
  st.error(
      f"Gagal memuat file `data.csv`. Pastikan file berada di folder yang"
      f" sama! Detail: {e}"
  )
  st.stop()


# 4. Sidebar untuk Filter Pilihan Kota & Tahun
st.sidebar.header("🌷 Filter Data")

# Mengambil list unik kota dan tahun untuk pilihan dropdown/multiselect
daftar_kota = sorted(df["Kota"].dropna().unique())
daftar_tahun = sorted(df["Tahun"].dropna().unique())

# Pilihan Filter di Sidebar
selected_kota = st.sidebar.multiselect(
    "Pilih Kota:", options=daftar_kota, default=daftar_kota[:3]
)
selected_tahun = st.sidebar.selectbox(
    "Pilih Tahun Minimal:", options=daftar_tahun, index=0
)

# Filter Data Berdasarkan Pilihan User
filtered_df = df[
    (df["Kota"].isin(selected_kota)) & (df["Tahun"] >= selected_tahun)
]


# 5. Menampilkan Metrik / Ringkasan Singkat
col1, col2, col3 = st.columns(3)
with col1:
  st.metric("Total Data Ditampilkan", f"{len(filtered_df)} baris")
with col2:
  st.metric("Jumlah Kota Dipilih", len(selected_kota))
with col3:
  st.metric("Tahun Mulai", selected_tahun)

st.divider()


# 6. Pembuatan Grafik Warna Pink Aesthetic
st.subheader("📊 Grafik Tren Data (Aesthetic Pink)")

if not filtered_df.empty:
  # Pilih kolom numerik selain 'Tahun' untuk dijadikan metrik grafik
  kolom_numerik = [
      col
      for col in filtered_df.select_dtypes(
          include=["float64", "int64"]
      ).columns
      if col != "Tahun"
  ]

  if kolom_numerik:
    y_axis = st.selectbox(
        "Pilih Indikator untuk Grafik:", options=kolom_numerik
    )

    # Membuat Line/Bar Chart dengan tema Pink menggunakan Plotly
    fig = px.line(
        filtered_df,
        x="Tahun",
        y=y_axis,
        color="Kota",
        markers=True,
        title=f"Perbandingan {y_axis} per Kota dari Tahun {selected_tahun}",
        color_discrete_sequence=px.colors.sequential.PuRd,  # Palet warna Pink ke Purple (Aesthetic)
    )

    # Kustomisasi background grafik agar selaras
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins", color="#444444"),
        title_font=dict(size=18, color="#d81b60"),
    )

    st.plotly_chart(fig, use_container_width=True)
  else:
    st.warning("Tidak ada kolom numerik yang tersedia untuk dibuat grafik.")
else:
  st.info(
      "Silakan pilih setidaknya satu kota di sidebar untuk menampilkan"
      " grafik."
  )


# 7. Menampilkan Tabel Data yang Telah Difilter
st.subheader("📋 Tabel Data Detail")
st.dataframe(filtered_df, use_container_width=True)
