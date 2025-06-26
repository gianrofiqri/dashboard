# Dashboard Analisis Program Studi Universitas 🎓

Dashboard interaktif untuk menganalisis data mahasiswa dan program studi menggunakan Streamlit.

## A. Penentuan Kebutuhan

### Pengguna Utama
- **Rektorat**: Untuk pengambilan keputusan strategis
- **Dosen**: Untuk evaluasi program studi
- **Staf Administrasi**: Untuk monitoring dan pelaporan
- **Publik**: Untuk transparansi informasi akademik

### Kebutuhan Informasi
- Distribusi mahasiswa per program studi
- Tingkat kelulusan setiap program
- Analisis berdasarkan jenis kelamin dan pendanaan
- Data untuk evaluasi kualitas pendidikan

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

File `Data mahasiswa.csv` harus berisi:
```csv
Pilihan 1,JK,bidikmisi,Lulus pada Prodi
Teknik Informatika,L,Reguler,Lulus
Sistem Informasi,P,Bidik Misi,Tidak Lulus
```

## GitHub Repository

Repository ini berisi:
- `Dashboard.py`: File utama dashboard
- `requirements.txt`: Dependencies
- `README.md`: Dokumentasi
- `data_sample.csv`: Contoh format data

### Cara Clone dan Gunakan
```bash
git clone https://github.com/gianrofiqri/dashboard
cd dashboard
pip install -r requirements.txt
streamlit run Dashboard.py
```

---

**Link Repository**: https://github.com/[username]/dashboard-universitas

⭐ Dashboard siap digunakan untuk analisis data akademik!
