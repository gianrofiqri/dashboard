# Dashboard Analisis Program Studi Universitas 

Dashboard interaktif untuk menganalisis data mahasiswa dan program studi menggunakan Streamlit.

## A. Penentuan Kebutuhan

### Pengguna Utama
- **Lembaga Pengembangan Universitas**: Untuk evaluasi program studi
- **Staf Administrasi**: Untuk monitoring dan pelaporan
- ** Dekan**: Monitoring tingkat kelulusan per program studi dalam fakultas 

## B. Perancangan Dashboard

### Data yang Ditampilkan
- **Total mahasiswa** dan jumlah program studi
- **Tingkat kelulusan** keseluruhan
- **Popularitas program studi** (pie chart)
- **Persentase kelulusan** per program (bar chart)

### Sumber Data
Data simulasi mahasiswa dengan kolom:
- `Pilihan 1`: Program Studi
- `JK`: Jenis Kelamin (L/P)
- `bidikmisi`: Status Pendanaan
- `Lulus pada Prodi`: Status Kelulusan

## C. Implementasi Teknis

### Teknologi
- **Python** dengan **Streamlit**
- **Pandas** untuk data processing
- **Plotly** untuk visualisasi

### Visualisasi (2 jenis)
1. **Pie Chart**: Distribusi mahasiswa per program studi
2. **Stacked Bar Chart**: Tingkat kelulusan per program studi

### Komponen Interaktif
- **Filter jenis kelamin**: Dropdown (Semua/Laki-laki/Perempuan)
- **Filter pendanaan**: Dropdown (Semua/Bidikmisi/Reguler)
- **Search box**: Pencarian program studi
- **Reset filter**: Kembali ke tampilan awal

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

File `Data mahasiswa.csv` berisi:
```csv
nomor_pendaftaran, JK, bidikmisi, Sekolah, Kabupaten, Provinsi, Pilihan 1, Pilihan 2, Ranking Sekolah, Nilai Mapel UN, Lulus pada Prodi, Lulus Pilihan, X1, X2, X3, X4, X5, X6, X7, X8, X9, XT, IP Sem 1, IP Sem 2, Predikat, Semester 1, Predikat Semester 2.

https://www.kaggle.com/datasets/achilham/data-mahasiswa?utm_source=chatgpt.com
```

## GitHub Repository

Repository ini berisi:
- `Dashboard.py`: File utama dashboard
- `requirements.txt`: Dependencies
- `README.md`: Dokumentasi
- `Data mahasiswa.csv`: Format data

### Cara Clone dan Gunakan
```bash
git clone https://github.com/gianrofiqri/dashboard.git
cd dashboard
pip install -r requirements.txt
streamlit run Dashboard.py
```

---

**Link Repository**: https://github.com/gianrofiqri/dashboard.git

