# DailyRoutine - Aplikasi Pelacak Kebiasaan Harian

![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)

Aplikasi desktop modern untuk membantu Anda membangun dan melacak kebiasaan positif setiap hari. Dibuat dengan Python dan PyQt5, DailyRoutine menawarkan antarmuka yang bersih, intuitif, dan fungsional.

![Tampilan Utama](docs/tampilan%20utama.png)

## Deskripsi

DailyRoutine adalah aplikasi yang dirancang untuk membantu pengguna mengelola dan memonitor kebiasaan harian mereka. Aplikasi ini memungkinkan pengguna untuk menambah, mengedit, menghapus, dan melacak kemajuan dari setiap kebiasaan. Dengan fitur visualisasi data yang kaya dan antarmuka yang ramah pengguna, membangun rutinitas positif menjadi lebih mudah dan menyenangkan.

Proyek ini dibuat untuk memenuhi tugas akhir mata kuliah Pemrograman Visual.

## Fitur Utama

- **Manajemen Kebiasaan**: Tambah, edit, dan hapus kebiasaan dengan mudah melalui dialog yang intuitif.
- **Tampilan Fleksibel**: Pilih antara tampilan petak (grid) atau daftar (list) untuk melihat kebiasaan Anda.
- **Pencarian dan Filter**: Cari kebiasaan secara spesifik atau filter berdasarkan kategori dan status.
- **Detail Kebiasaan**: Lihat detail lengkap, termasuk riwayat progres dan statistik untuk setiap kebiasaan.
- **Ekspor Data**: Ekspor daftar kebiasaan Anda ke format PDF atau CSV untuk laporan atau arsip.
- **Statistik Visual**: Papan statistik memberikan ringkasan tentang total kebiasaan, kebiasaan yang selesai, dan tingkat penyelesaian secara keseluruhan.
- **Desain Modern**: Antarmuka yang bersih dan modern dibangun dengan Qt for Python (PyQt5).

## Galeri Screenshot

| Tambah Kebiasaan Baru | Edit Kebiasaan |
| :---: | :---: |
| ![Tambah Kebiasaan](docs/add%20new%20habbit.png) | ![Edit Kebiasaan](docs/edit%20habbit.png) |

| Lihat Detail Kebiasaan | Tampilan Daftar & Petak |
| :---: | :---: |
| ![Detail Kebiasaan](docs/detail%20habbit.png) | ![Tampilan Pilihan](docs/show%20by%5Bcard%7Clist%5D.png) |

| Filter Data | Ekspor ke PDF & CSV |
| :---: | :---: |
| ![Filter Kebiasaan](docs/filter%20data.png) | ![Hasil Ekspor](docs/view%20pdf%20exported.png) |

## Teknologi yang Digunakan

- **Python**: Bahasa pemrograman utama.
- **PyQt5**: Kerangka kerja GUI untuk membangun antarmuka desktop.
- **SQLite**: Sistem manajemen basis data untuk penyimpanan data lokal.

## Instalasi dan Penggunaan

Ikuti langkah-langkah di bawah ini untuk menjalankan aplikasi di lingkungan lokal Anda.

### 1. Prasyarat

- [Python](https://www.python.org/downloads/) (versi 3.7 atau lebih baru)
- `pip` (biasanya terinstal bersama Python)
- `venv` (biasanya terinstal bersama Python)

### 2. Kloning Repositori

```bash
# (Opsional) Jika menggunakan git
git clone https://github.com/devChampl00/pv25-finalproject-DailyRoutine
cd pv25-finalproject-DailyRoutine
```
Atau, cukup unduh dan ekstrak file proyek dalam folder `pv25-finalproject-DailyRoutine`.

### 3. Buat dan Aktifkan Virtual Environment (Opsional)

Sangat disarankan untuk menggunakan lingkungan virtual untuk mengisolasi dependensi proyek, biasanya digunakan di Sistem Operasi Linux.

```bash
# Membuat virtual environment
python -m venv venv

# Mengaktifkan di Windows
venv\\Scripts\\activate

# Mengaktifkan di macOS/Linux
source venv/bin/activate
```

### 4. Instal Dependensi

Dengan virtual environment yang aktif, instal semua paket yang diperlukan dari file `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 5. Inisialisasi dan Isi Database (Opsional)

Aplikasi akan secara otomatis membuat file database kosong saat pertama kali dijalankan. Jika Anda ingin memulai dengan beberapa data contoh, jalankan skrip `seed_database.py`.

```bash
python seed_database.py
```

### 6. Jalankan Aplikasi

Setelah semua dependensi terinstal, Anda dapat menjalankan aplikasi utama.

```bash
python main.py
```

## Informasi Pengembang

- **Nama**: UMAM ALPARIZI
- **NIM**: F1D02310141
- **Email**: [f1d02310141@student.unram.ac.id](mailto:f1d02310141@student.unram.ac.id)
