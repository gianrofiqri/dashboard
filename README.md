# Dashboard Analisis Pendaftaran Mahasiswa Universitas Bandung 2023

Dashboard interaktif untuk menganalisis data pendaftaran mahasiswa dan tingkat penerimaan program studi menggunakan Streamlit.

## A. Penentuan Kebutuhan

### Pengguna Utama
- **Calon Mahasiswa**: Untuk melihat tingkat persaingan dan peluang diterima di program studi
- **Lembaga Penerimaan Mahasiswa**: Untuk evaluasi tingkat penerimaan program studi
- **Staf Administrasi**: Untuk monitoring dan pelaporan data pendaftaran
- **Pimpinan Universitas**: Monitoring popularitas dan tingkat penerimaan per program studi

## B. Perancangan Dashboard

### Data yang Ditampilkan
- **Total pendaftar** dan jumlah program studi
- **Jumlah yang diterima** dan tingkat penerimaan keseluruhan
- **Distribusi pendaftar** per program studi (pie chart)
- **Tingkat penerimaan** per program studi (bar chart)
- **Tabel ringkasan lengkap** dengan kategori peluang

### Sumber Data
Data pendaftaran mahasiswa dengan kolom:
- `Pilihan 1`: Program Studi pilihan pertama
- `bidikmisi`: Status Pendanaan (Bidik Misi/Reguler)
- `Provinsi`: Asal provinsi pendaftar
- `Lulus pada Prodi`: Status kelulusan/penerimaan

## C. Implementasi Teknis

### Teknologi
- **Python** dengan **Streamlit**
- **Pandas** untuk data processing
- **Plotly Express & Graph Objects** untuk visualisasi interaktif

### Visualisasi (2 jenis utama)
1. **Pie Chart**: Distribusi pendaftar per program studi dengan informasi persentase
2. **Bar Chart**: Tingkat penerimaan per program studi dengan skala 0-100%

### Komponen Interaktif
- **Filter jenis pendanaan**: Dropdown (Semua/Bidikmisi/Reguler)
- **Filter asal provinsi**: Dropdown dengan semua provinsi tersedia
- **Search box**: Pencarian program studi dalam tabel ringkasan
- **Reset filter**: Tombol untuk kembali ke tampilan awal
- **Download CSV**: Ekspor data hasil filter

### Fitur Dashboard
- **Metrics Cards**: Menampilkan statistik utama dengan desain menarik
- **Sidebar Filter**: Panel filter dengan statistik data terpilih dan progress bar
- **Tabel Interaktif**: Ringkasan lengkap dengan ranking dan kategori peluang
- **Responsive Design**: Layout yang menyesuaikan dengan ukuran layar

## D. Cara Menjalankan

### Install Dependencies
```bash
pip install streamlit pandas plotly
```

### Jalankan Dashboard
```bash
streamlit run Dashboard.py
```

### Akses Dashboard
Buka browser: `http://localhost:8501`

## Format Data

File `Data mahasiswa.csv` harus berisi kolom minimum:
```csv
Pilihan 1, bidikmisi, Provinsi, Sekolah, Lulus pada Prodi
```

**Kolom Penting:**
- `Pilihan 1`: Program studi yang dipilih pendaftar
- `bidikmisi`: Status pendanaan ("Bidik Misi" atau lainnya)
- `Provinsi`: Provinsi asal pendaftar
- `Lulus pada Prodi`: Status penerimaan (kosong/"Tidak Lulus" = tidak diterima)

**Sumber Data**: [Kaggle - Data Mahasiswa](https://www.kaggle.com/datasets/achilham/data-mahasiswa)

## Fitur Analisis

### Kategori Peluang Penerimaan
- **Peluang Tinggi**: Tingkat penerimaan ≥ 70%
- **Peluang Sedang**: Tingkat penerimaan 40-69%
- **Peluang Rendah**: Tingkat penerimaan < 40%

### Statistik yang Disediakan
- Ranking program studi berdasarkan jumlah pendaftar
- Persentase tingkat penerimaan per program studi
- Jumlah pendaftar Bidikmisi per program studi
- Analisis persaingan untuk setiap program studi

## GitHub Repository

Repository ini berisi:
- `Dashboard.py`: File utama dashboard dengan semua fungsi analisis
- `requirements.txt`: Dependencies yang diperlukan
- `README.md`: Dokumentasi lengkap
- `Data mahasiswa.csv`: File data

### Cara Clone dan Gunakan
```bash
git clone https://github.com/gianrofiqri/dashboard.git
cd dashboard
pip install -r requirements.txt
# Pastikan file 'Data mahasiswa.csv' tersedia di direktori yang sama
streamlit run Dashboard.py
```

### Requirements.txt
```txt
streamlit
pandas
plotly
```

**Link Repository**: https://github.com/gianrofiqri/dashboard.git