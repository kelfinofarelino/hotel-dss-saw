# 🏨 Sistem Cerdas Pendukung Keputusan Pemilihan Hotel di Bali

Repositori ini berisi proyek akhir untuk mata kuliah **Praktikum Sistem Cerdas Pendukung Keputusan** (Plug H). Aplikasi ini merupakan Sistem Pendukung Keputusan (SPK) berbasis web yang dibangun menggunakan **Streamlit** dan menerapkan metode **Simple Additive Weighting (SAW)** untuk memberikan rekomendasi pemilihan hotel terbaik di Bali menggunakan data riil hasil *scraping* dari platform Tiket.com.

---

## 👥 Identitas Kelompok (Plug-H)
Proyek ini dikembangkan oleh:
* **Adhafa Joan Putranto** (123240069) — [GitHub Profile](https://github.com/adhafajp)
* **Muhammad Farelino Kelfin** (123240205) — [GitHub Profile](https://github.com/kelfinofarelino)

---

## ✨ Fitur Utama
Aplikasi SPK ini dilengkapi dengan antarmuka grafis (GUI) berbasis web yang interaktif dengan fitur-fitur unggulan berikut:

* **Navigasi Layout Terstruktur (Tabs):** Memisahkan alur pemrosesan data secara rapi ke dalam 5 halaman (*Profil Kelompok, Matriks Keputusan X, Normalisasi R, Hasil Perangkingan V, dan Visualisasi*).
* **Tampilan Dataset Interaktif:** Menyajikan visualisasi data mentah hotel dan hasil kalkulasi matriks dalam bentuk tabel dinamis yang dapat di-*sort* atau diperbesar menggunakan `st.dataframe`.
* **Input Bobot Dinamis:** Pengguna dapat menyesuaikan proporsi bobot untuk 5 kriteria berbeda melalui komponen interaktif di *sidebar* (kombinasi `st.slider` dan `st.number_input`) lengkap dengan sistem validasi total nilai wajib berjumlah 100.
* **Eksekusi Manual (*On-Demand*):** Perhitungan rumus matematis SAW diikat menggunakan tombol eksekusi (`st.button`). Proses kalkulasi hanya berjalan jika tombol ditekan, sehingga menghemat *resource* memori dan mencegah kalkulasi otomatis yang berat setiap kali bobot digeser.
* **Visualisasi Peringkat:** Menampilkan grafik batang (*Bar Chart*) interaktif untuk membandingkan nilai preferensi akhir dari **Top 15 Hotel Terbaik** di Bali.
* **Mekanisme Pengolahan Data Kebal Error (*Robust Data Cleaning*):** Kode dibekali fungsi penanganan otomatis terhadap karakter gaib (*Byte Order Mark* via `utf-8-sig`), pencarian kolom berbasis pencocokan teks kata kunci (*fuzzy matching*), serta konversi otomatis tanda desimal koma (`,`) khas dataset lokal menjadi tanda titik (`.`) agar dapat diproses secara matematis oleh Python.

---

## 💾 Link Dataset
Dataset yang digunakan dalam sistem ini diambil dari Kaggle:
* **Source:** [Hotel Listings in Bali (Scraped Data from Tiket.com)](https://www.kaggle.com/datasets/anisyanugraheni/hotel-listings-in-bali-scraped-data)
* **File Name:** `Updated_ScrapingHotelTiketcom.csv` (Mencakup data nama hotel riil beserta parameter harganya).

---

## 📊 Kriteria Penilaian (SAW)
Sistem ini menggunakan 5 kriteria utama untuk menentukan nilai utilitas hotel:
1. **C1 - Harga (*Price Starts From*):** Atribut *Cost* (Semakin murah harga sewa kamar, semakin baik).
2. **C2 - Rating:** Atribut *Benefit* (Semakin tinggi skor penilaian pengunjung, semakin baik).
3. **C3 - Star / Bintang:** Atribut *Benefit* (Semakin tinggi tingkatan kelas bintang hotel, semakin baik).
4. **C4 - Jumlah Ulasan (*Review Count*):** Atribut *Benefit* (Semakin banyak jumlah ulasan, mengindikasikan tingkat kepercayaan hotel yang semakin baik).
5. **C5 - Fasilitas (*Facilities*):** Atribut *Benefit* (Sistem menghitung secara dinamis total jumlah fasilitas yang tersedia dari baris teks data. Semakin lengkap fasilitasnya, semakin baik).

---

## 🛠️ Teknologi yang Digunakan
* **Bahasa Pemrograman:** Python 3.12+
* **Framework GUI:** Streamlit
* **Pustaka Analisis Data:** Pandas, NumPy

---
