# 📚 Sistem Rekomendasi Konversi Mata Kuliah Berbasis NLP  
### Menggunakan Metode BERT di Universitas Islam Balitar

Proyek ini merupakan implementasi sistem rekomendasi berbasis *Natural Language Processing (NLP)* untuk mempermudah proses konversi mata kuliah mahasiswa transfer. Sistem ini memanfaatkan model **BERT** untuk memahami makna deskripsi mata kuliah dan mencocokkannya dengan data kurikulum Universitas Islam Balitar.

---

## 🚀 Fitur Utama

- **Pencocokan Otomatis Deskripsi Mata Kuliah**  
  Memanfaatkan model BERT untuk memahami semantik dan menghitung kemiripan antar teks secara cerdas.

- **Pengukuran Kemiripan dengan Cosine Similarity**  
  Mengidentifikasi mata kuliah paling relevan berdasarkan kedekatan makna.

- **Antarmuka Interaktif (Streamlit)**  
  Visualisasi hasil rekomendasi yang mudah digunakan dan informatif.

- **Statistik Ringkasan**  
  Menampilkan total mata kuliah, jumlah SKS, dan semester hasil konversi.

---

## 🛠 Teknologi yang Digunakan

- Python
- Transformers (HuggingFace BERT)
- scikit-learn
- Streamlit
- Pandas & NumPy

---

## 🧠 Cara Kerja Singkat

1. Input deskripsi mata kuliah mahasiswa dan kurikulum universitas.
2. Semua teks diproses dan di-*embedding* menggunakan model BERT.
3. Kemiripan antar deskripsi dihitung menggunakan *cosine similarity*.
4. Sistem merekomendasikan mata kuliah terdekat berdasarkan skor kemiripan tertinggi.

---

## 📎 Tujuan Proyek

Proyek ini bertujuan untuk meningkatkan akurasi dan efisiensi proses konversi mata kuliah bagi mahasiswa pindahan, dengan memanfaatkan kemampuan pemahaman konteks bahasa alami melalui pendekatan NLP modern.

> Untuk menjalankan aplikasi, pastikan semua dependensi telah diinstal dan jalankan dengan:
> 
> ```bash
> streamlit run app.py
> ```

