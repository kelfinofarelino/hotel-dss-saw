import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# 1. KONFIGURASI UTAMA & GUI
# ==========================================
st.set_page_config(
    page_title="SPK Hotel Bali | SAW", 
    page_icon="🏨", 
    layout="wide"
)

st.title("🏨 Sistem Cerdas Pendukung Keputusan Pemilihan Hotel di Bali")
st.markdown(
    """
    Aplikasi ini menggunakan metode **Simple Additive Weighting (SAW)** untuk memberikan rekomendasi 
    hotel terbaik di Bali menggunakan data riil (beserta nama asli hotel).
    """
)

# ==========================================
# 2. FUNGSI LOGIKA METODE SAW
# ==========================================
@st.cache_data
def load_and_preprocess_data(file_path):
    # 1. Baca data & usir karakter gaib (BOM)
    df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig', on_bad_lines='skip')
    
    if len(df.columns) == 1:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
        
    # 2. PENCARIAN KOLOM OTOMATIS
    col_title = [c for c in df.columns if 'Title' in c][0]
    col_price = [c for c in df.columns if 'Price' in c][0]
    col_rating = [c for c in df.columns if 'Rating' in c][0]
    col_review = [c for c in df.columns if 'Review' in c][0]
    col_star = [c for c in df.columns if 'Star' in c][0]
    
    kriteria_kolom = [col_title, col_price, col_rating, col_review, col_star]
    
    # 3. Filter data kriteria
    df = df.dropna(subset=kriteria_kolom).head(300).copy()
    df['Alternatif (Hotel)'] = df[col_title]
    
    # 4. Olah kolom Fasilitas jadi angka
    col_fac = [c for c in df.columns if 'Facilit' in c]
    if col_fac:
        df['Jumlah Fasilitas'] = df[col_fac[0]].apply(lambda x: len(str(x).split(',')) if pd.notnull(x) else 1)
    else:
        df['Jumlah Fasilitas'] = 1
        
    columns_to_keep = [
        'Alternatif (Hotel)', 
        col_price, 
        col_rating, 
        col_star, 
        col_review,
        'Jumlah Fasilitas'
    ]
    
    df_raw = df[columns_to_keep].copy()
    
    # 5. RENAME PAKSA
    df_matrix = df_raw.copy()
    df_matrix.columns = [
        'Alternatif (Hotel)', 
        'C1 (Harga)', 
        'C2 (Rating)', 
        'C3 (Bintang)', 
        'C4 (Ulasan)', 
        'C5 (Fasilitas)'
    ]
    
    # 6. PEMBERSIHAN ANGKA (Solusi Error '4,8')
    # a. Bersihkan C1 (Harga) - Hapus huruf, titik ribuan, Rp (sisakan angka murni)
    df_matrix['C1 (Harga)'] = df_matrix['C1 (Harga)'].astype(str).replace(r'[^\d]', '', regex=True)
    
    # b. Ganti koma (,) menjadi titik (.) agar dikenali Python sebagai desimal
    for col in ['C2 (Rating)', 'C3 (Bintang)', 'C4 (Ulasan)']:
        df_matrix[col] = df_matrix[col].astype(str).str.replace(',', '.')
        
    # c. Ubah SEMUA kriteria menjadi format angka ukur baku (Float)
    for col in df_matrix.columns:
        if col != 'Alternatif (Hotel)':
            df_matrix[col] = pd.to_numeric(df_matrix[col], errors='coerce')
            
    df_matrix = df_matrix.dropna()
    
    df_matrix.set_index('Alternatif (Hotel)', inplace=True)
    return df_raw, df_matrix

def calculate_normalization(df_matrix, atribut):
    df_norm = df_matrix.copy().astype(float)
    for i, col in enumerate(df_matrix.columns):
        if atribut[i] == 0:  # Atribut Cost
            min_val = df_matrix[col].min()
            df_norm[col] = min_val / df_matrix[col]
        else:  # Atribut Benefit
            max_val = df_matrix[col].max()
            df_norm[col] = df_matrix[col] / max_val
    return df_norm

def calculate_final_score(df_matrix, df_norm, weights):
    W = np.array(weights)
    scores = df_norm.values.dot(W) 
    
    df_final = df_matrix.copy()
    df_final['Skor Akhir'] = scores
    df_final = df_final.reset_index()
    df_final = df_final.sort_values(by='Skor Akhir', ascending=False).reset_index(drop=True)
    return df_final

# ==========================================
# 3. PEMUATAN DATASET
# ==========================================
try:
    # Memanggil dataset dari dalam folder dataset
    df_raw, df_matrix = load_and_preprocess_data("dataset/Updated_ScrapingHotelTiketcom.csv")
except FileNotFoundError:
    st.error("❌ Dataset tidak ditemukan. Pastikan file CSV Bali berada di dalam folder 'dataset/'.")
    st.stop()

# ==========================================
# 4. SIDEBAR (Widget Dinamis)
# ==========================================
st.sidebar.header("⚙️ Pengaturan Bobot Kriteria")
st.sidebar.markdown("Total seluruh kriteria harus berjumlah tepat 100.")
st.sidebar.markdown("---")

w_c1 = st.sidebar.slider("Bobot C1 (Harga) [Cost]", 0, 100, 30, step=5)
w_c2 = st.sidebar.slider("Bobot C2 (Rating) [Benefit]", 0, 100, 20, step=5)
w_c3 = st.sidebar.slider("Bobot C3 (Bintang) [Benefit]", 0, 100, 15, step=5)
w_c4 = st.sidebar.number_input("Bobot C4 (Ulasan) [Benefit]", min_value=0, max_value=100, value=15, step=5)
w_c5 = st.sidebar.number_input("Bobot C5 (Fasilitas) [Benefit]", min_value=0, max_value=100, value=20, step=5)

total_bobot = w_c1 + w_c2 + w_c3 + w_c4 + w_c5
st.sidebar.markdown("---")

is_weight_valid = (total_bobot == 100)

if not is_weight_valid:
    st.sidebar.error(f"⚠️ Total bobot: **{total_bobot}**. Jumlah harus 100.")
else:
    st.sidebar.success("✅ Total bobot valid (100).")

W = [w_c1 / 100, w_c2 / 100, w_c3 / 100, w_c4 / 100, w_c5 / 100]
atribut = [0, 1, 1, 1, 1]  # Harga adalah Cost (0), sisanya Benefit (1)

df_norm = calculate_normalization(df_matrix, atribut)

# ==========================================
# 5. TABS & PERHITUNGAN
# ==========================================
tab_profil, tab_data, tab_norm, tab_hitung, tab_grafik = st.tabs([
    "👥 Profil Kelompok", "📊 Matriks (X)", "🔄 Normalisasi (R)", "🏆 Hasil (V)", "📈 Visualisasi"
])

with tab_profil:
    st.subheader("👥 Profil Anggota Kelompok Pengembang")
    col1, col2 = st.columns(2)
    with col1:
        st.info("### Anggota 1\n* **Nama:** Adhafa Joan Putranto\n* **NIM:** 123240069\n* **Peran:** Data Preprocessing & Analis Model")
    with col2:
        st.success("### Anggota 2\n* **Nama:** Muhammad Farelino Kelfin\n* **NIM:** 123240205\n* **Peran:** Developer GUI Streamlit & Algoritma Sistem")

with tab_data:
    st.subheader("1. Matriks Keputusan Awal (X)")
    st.dataframe(df_matrix, use_container_width=True)

with tab_norm:
    st.subheader("2. Matriks Hasil Normalisasi (R)")
    st.dataframe(
        df_norm.style.format("{:.4f}"),
        use_container_width=True
    )

with tab_hitung:
    st.subheader("3. Perhitungan Nilai Preferensi (V)")
    
    if is_weight_valid:
        hitung_button = st.button("🚀 Hitung Perangkingan SPK", type="primary")
        if hitung_button:
            st.session_state['df_final_result'] = calculate_final_score(df_matrix, df_norm, W)
            st.success("🎉 Berhasil dieksekusi!")
            
        if 'df_final_result' in st.session_state:
            df_display = st.session_state['df_final_result']
            st.dataframe(
                df_display.style.format({
                    "Skor Akhir": "{:.4f}",
                    "C1 (Harga)": "Rp {:,.0f}",
                    "C2 (Rating)": "{:.1f}",
                    "C3 (Bintang)": "{:.0f}",
                    "C4 (Ulasan)": "{:.0f}",
                    "C5 (Fasilitas)": "{:.0f}"
                }).background_gradient(cmap="Greens", subset=["Skor Akhir"]),
                use_container_width=True
            )
            top_alt = df_display.iloc[0]['Alternatif (Hotel)']
            top_score = df_display.iloc[0]['Skor Akhir']
            st.success(f"🏅 **Rekomendasi Terbaik:** Hotel **{top_alt}** dengan nilai **{top_score:.4f}**.")
    else:
        st.error("❌ Sesuaikan bobot hingga total 100 untuk menghitung.")

with tab_grafik:
    st.subheader("4. Top 15 Hotel Terbaik")
    if is_weight_valid and 'df_final_result' in st.session_state:
        df_chart = st.session_state['df_final_result'].head(15)
        chart_data = df_chart[['Alternatif (Hotel)', 'Skor Akhir']].set_index('Alternatif (Hotel)')
        st.bar_chart(chart_data, color="#2ECC71")
    else:
        st.info("Hitung data terlebih dahulu di Tab Hasil.")