import os
import pandas as pd
import streamlit as st

# 1. Konfigurasi Halaman Dashboard (Lebar & Custom Icon)
st.set_page_config(
    page_title="Executive Pink Analytics Dashboard", page_icon="🌸", layout="wide"
)

# 2. Custom CSS untuk Tema Pink Professional & Aesthetic
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;450;600;700&family=Playfair+Display:ital,wght@0,600;1,400&display=swap');

    /* Global Font & Background */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Judul Utama */
    .main-title {
        font-family: 'Playfair Display', serif;
        color: #d81b60;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: -5px;
    }
    
    .main-subtitle {
        color: #888888;
        font-size: 15px;
        margin-bottom: 30px;
    }

    /* Styling Metric Card Kustom */
    .metric-card {
        background-color: #fff0f5;
        border: 1px solid #ffb6c1;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(255, 182, 193, 0.15);
    }
    .metric-title {
        font-size: 13px;
        color: #ad1457;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 24px;
        color: #880e4f;
        font-weight: 700;
        margin-top: 5px;
    }

    /* Header Section */
    h2, h3 {
        color: #c2185b !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #fff9fb;
        border-right: 1px solid #ffe4e1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Load Data Secara Aman (Mendukung path relatif file.py)
@st.cache_data
def load_data():
  dir_path = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(dir_path, "data.csv")
  return pd.read_csv(file_path)


try:
  df = load_data()
except Exception as e:
  st.error(
      f"❌ Gagal memuat file `data.csv`. Pastikan file berada di folder yang"
      f" sama dengan `file.py`. Detail error: {e}"
  )
  st.stop()

# 4. Sidebar Kontrol & Filter Profesional
st.sidebar.markdown(
    "<h2 style='text-align: center; color: #d81b60;'>🌷 Control Panel</h2>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

daftar_kota = sorted(df["Kota"].dropna().unique())
daftar_tahun = sorted(df["Tahun"].dropna().unique())

# Pilihan Menu Utama di Sidebar
menu = st.sidebar.radio(
    "Navigasi Dashboard",
    [
        "📈 Overview & Tren",
        "⚖️ Perbandingan Antar Kota",
        "🔍 Eksplorasi Data Analisis (EDA)",
        "📋 Tabel Data Mentah",
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Filter Parameter")

selected_kota = st.sidebar.multiselect(
    "Pilih Kota:", options=daftar_kota, default=daftar_kota[:3]
)
selected_tahun = st.sidebar.slider(
    "Rentang Tahun:",
    min_value=int(min(daftar_tahun)),
    max_value=int(max(daftar_tahun)),
    value=(int(min(daftar_tahun)), int(max(daftar_tahun))),
)

# Filter Data Berdasarkan Sidebar
filtered_df = df[
    (df["Kota"].isin(selected_kota))
    & (df["Tahun"] >= selected_tahun[0])
    & (df["Tahun"] <= selected_tahun[1])
]

# Identifikasi Kolom Numerik untuk Analisis
kolom_numerik = [
    col
    for col in filtered_df.select_dtypes(include=["float64", "int64"]).columns
    if col != "Tahun"
]

# ==========================================
# HALAMAN 1: OVERVIEW & TREN
# ==========================================
if menu == "📈 Overview & Tren":
  st.markdown(
      '<p class="main-title">✨ Executive Analytics Dashboard</p>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<p class="main-subtitle">Analisis tren data komprehensif dengan'
      " performa visual bernuansa pink.</p>",
      unsafe_allow_html=True,
  )

  # Ringkasan Metrics Cards
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.markdown(
        f"""
            <div class="metric-card">
                <div class="metric-title">Total Observasi</div>
                <div class="metric-value">{len(filtered_df)}</div>
            </div>""",
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        f"""
            <div class="metric-card">
                <div class="metric-title">Kota Dipilih</div>
                <div class="metric-value">{len(selected_kota)}</div>
            </div>""",
        unsafe_allow_html=True,
    )
  with col3:
    rata_tahun = (
        int(filtered_df["Tahun"].mean()) if not filtered_df.empty else 0
    )
    st.markdown(
        f"""
            <div class="metric-card">
                <div class="metric-title">Rata-rata Tahun</div>
                <div class="metric-value">{rata_tahun}</div>
            </div>""",
        unsafe_allow_html=True,
    )
  with col4:
    total_kolom = len(kolom_numerik)
    st.markdown(
        f"""
            <div class="metric-card">
                <div class="metric-title">Indikator Metrik</div>
                <div class="metric-value">{total_kolom}</div>
            </div>""",
        unsafe_allow_html=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)

  if not filtered_df.empty and kolom_numerik:
    st.subheader("📊 Grafik Tren Waktu per Indikator")
    y_axis = st.selectbox(
        "Pilih Indikator Metrik untuk Dianiaya:", options=kolom_numerik
    )

    # Pivot data untuk grafik garis Streamlit
    chart_data = filtered_df.pivot(
        index="Tahun", columns="Kota", values=y_axis
    )
    st.line_chart(
        chart_data, color=["#ff69b4", "#ff1493", "#db7093", "#ffb6c1", "#c71585"]
    )
  else:
    st.warning("Silakan pilih minimal satu kota dan pastikan data tersedia.")

# ==========================================
# HALAMAN 2: PERBANDINGAN ANTAR KOTA
# ==========================================
elif menu == "⚖️ Perbandingan Antar Kota":
  st.markdown(
      '<p class="main-title">⚖️ Analisis Perbandingan Antar Kota</p>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<p class="main-subtitle">Evaluasi komparatif performa indikator di'
      " berbagai wilayah terpilih.</p>",
      unsafe_allow_html=True,
  )

  if len(selected_kota) >= 1 and kolom_numerik:
    col_a, col_b = st.columns(2)
    with col_a:
      pilih_Indikator = st.selectbox(
          "Pilih Indikator Komparasi:", options=kolom_numerik, key="comp_ind"
      )
    with col_b:
      pilih_tahun_satu = st.selectbox(
          "Pilih Tahun Spesifik:",
          options=sorted(filtered_df["Tahun"].unique(), reverse=True),
          key="comp_year",
      )

    # Filter data khusus tahun tersebut
    df_komparasi = filtered_df[filtered_df["Tahun"] == pilih_tahun_satu]

    if not df_komparasi.empty:
      st.markdown(f"### Grafik Batang Perbandingan Tahun {pilih_tahun_satu}")
      bar_data = (
          df_komparasi.set_index("Kota")[pilih_Indikator]
          .reset_index()
          .rename(columns={pilih_Indikator: "Nilai"})
      )
      st.bar_chart(
          bar_data.set_index("Kota"), color="#ff69b4", use_container_width=True
      )

      st.markdown("### 📋 Ringkasan Nilai Komparasi")
      st.dataframe(
          df_komparasi[["Kota", "Tahun", pilih_Indikator]],
          use_container_width=True,
      )
    else:
      st.info("Tidak ada data pada tahun dan kota yang dipilih.")
  else:
    st.warning(
        "Harap pilih minimal satu kota di control panel sidebar sebelah kiri."
    )

# ==========================================
# HALAMAN 3: EKSPLORASI DATA ANALISIS (EDA)
# ==========================================
elif menu == "🔍 Eksplorasi Data Analisis (EDA)":
  st.markdown(
      '<p class="main-title">🔍 Eksplorasi Data Analisis (EDA)</p>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<p class="main-subtitle">Statistik deskriptif, distribusi nilai, dan'
      " korelasi antar variabel.</p>",
      unsafe_allow_html=True,
  )

  if not filtered_df.empty and kolom_numerik:
    tab1, tab2 = st.tabs(
        ["📈 Statistik Deskriptif", "🔗 Matriks Korelasi Antar Variabel"]
    )

    with tab1:
      st.subheader("Ringkasan Statistik Deskriptif")
      desc_stats = filtered_df[kolom_numerik].describe()
      # Styling tabel agar bernuansa pink lembut
      st.dataframe(
          desc_stats.style.background_gradient(cmap="PuRd"),
          use_container_width=True,
      )

    with tab2:
      st.subheader("Analisis Korelasi Pearson")
      corr_matrix = filtered_df[kolom_numerik].corr()
      st.dataframe(
          corr_matrix.style.background_gradient(cmap="RdPu", vmin=-1, vmax=1),
          use_container_width=True,
      )
      st.caption(
          "Catatan: Nilai mendekati 1 atau -1 menunjukkan hubungan linier"
          " yang kuat antar indikator keuangan/daerah."
      )
  else:
    st.warning("Data atau kolom numerik tidak mencukupi untuk analisis EDA.")

# ==========================================
# HALAMAN 4: TABEL DATA MENTAH
# ==========================================
elif menu == "📋 Tabel Data Mentah":
  st.markdown(
      '<p class="main-title">📋 Eksplorasi Dataset Lengkap</p>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<p class="main-subtitle">Seluruh rekaman data terfilter yang tersimpan'
      " dalam sistem.</p>",
      unsafe_allow_html=True,
  )

  st.dataframe(filtered_df, use_container_width=True)

  # Tombol Download CSV
  csv_export = filtered_df.to_csv(index=False).encode("utf-8")
  st.download_button(
      label="📥 Download Data Terfilter as CSV",
      data=csv_export,
      file_name="data_filtered_dashboard.csv",
      mime="text/csv",
  )
