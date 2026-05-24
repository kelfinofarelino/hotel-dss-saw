# 🏨 Sistem Cerdas Pendukung Keputusan Pemilihan Hotel

Repositori ini berisi proyek akhir untuk mata kuliah **Praktikum Sistem Cerdas Pendukung Keputusan**. Aplikasi ini merupakan Sistem Pendukung Keputusan (SPK) berbasis web yang dibangun menggunakan **Streamlit** dan menerapkan metode **Simple Additive Weighting (SAW)** untuk memberikan rekomendasi pemilihan hotel terbaik di Jakarta.

---

## 👥 Identitas Kelompok (Plug-H)
Proyek ini dikembangkan oleh:
* **Adhafa Joan Putranto** (123240069) (https://github.com/adhafajp)
* **Muhammad Farelino Kelfin** (123240205) (https://github.com/kelfinofarelino)

---

## ✨ Fitur Utama
Aplikasi SPK ini dilengkapi dengan antarmuka grafis (GUI) yang interaktif dengan fitur-fitur berikut:
* **Navigasi Tab Terstruktur:** Proses perhitungan metode SAW dipisahkan secara rapi ke dalam beberapa tab (Matriks Keputusan Awal, Normalisasi, Hasil Akhir/Perangkingan, dan Visualisasi).
* **Tampilan Dataset Interaktif:** Menampilkan data mentah hotel dan hasil perhitungan matriks dalam bentuk tabel dinamis.
* **Input Bobot Dinamis:** Pengguna dapat menyesuaikan bobot untuk 5 kriteria berbeda melalui *sidebar* (dengan validasi total bobot wajib bernilai 100).
* **Eksekusi Manual (*On-Demand*):** Perhitungan SPK dan visualisasi dikendalikan oleh pengguna melalui tombol eksekusi untuk efisiensi *resource*.
* **Visualisasi Peringkat:** Menampilkan grafik (Bar Chart) interaktif untuk Top 15 Hotel terbaik berdasarkan skor preferensi akhir.

---

## 💾 Link Dataset:
https://www.kaggle.com/datasets/muhammadgusanwaakbar/traveloka-hotel-list-jakarta

---

## 📊 Kriteria Penilaian (SAW)
Sistem ini menggunakan 5 kriteria utama dalam proses seleksi hotel:
1. **C1 - Harga:** Atribut *Cost* (Semakin murah semakin baik)
2. **C2 - Rating:** Atribut *Benefit* (Semakin tinggi semakin baik)
3. **C3 - Star / Bintang:** Atribut *Benefit* (Semakin tinggi semakin baik)
4. **C4 - Jumlah Reviews:** Atribut *Benefit* (Semakin banyak semakin baik)
5. **C5 - Fasilitas:** Atribut *Benefit* (Semakin lengkap semakin baik)

---

## 🛠️ Teknologi yang Digunakan
* **Bahasa Pemrograman:** Python
* **Framework GUI:** Streamlit
* **Pengolahan Data:** Pandas, NumPy

---