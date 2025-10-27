# Aplikasi Desktop Catatan Harian

Aplikasi desktop sederhana berbasis PyQt5 untuk mencatat dan mengelola catatan harian. Aplikasi ini memungkinkan pengguna untuk membuat, menyimpan, dan melihat catatan dengan kategori dan tanda penting.

## Fitur

- Membuat catatan dengan judul, kategori, dan konten
- Menandai catatan sebagai penting
- Menyimpan catatan secara lokal dalam format JSON
- Melihat daftar catatan yang telah disimpan
- Memfilter catatan berdasarkan kategori
- Mencari catatan tertentu
- Antarmuka pengguna yang sederhana dan bersih
- Menampilkan NIM dan nama mahasiswa pada antarmuka (tidak dapat diedit oleh pengguna)
- Menggunakan setStyleSheet() untuk meningkatkan tampilan visual

## Persyaratan

- Python 3.6 atau lebih tinggi
- PyQt5

## Instalasi

1. Clone atau unduh repositori ini.
2. Instal paket yang diperlukan:

   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan aplikasi:

   ```bash
   python main.py
   ```

## Struktur Proyek

- `main.py` - Titik masuk utama untuk aplikasi.
- `ui_main.py` - Komponen UI utama dan logika aplikasi.
- `style.py` - Stylesheet seperti CSS untuk aplikasi.
- `note_data_manager.py` - Mengelola operasi data catatan (simpan, muat, cari).
- `widgets.py` - Widget kustom yang digunakan dalam aplikasi.
- `notes_data.json` - Penyimpanan lokal untuk data catatan.

## Cara Penggunaan

1. Masukkan judul untuk catatan Anda.
2. Pilih kategori dari dropdown (Personal, Work, School).
3. Centang kotak "Important" jika catatan tersebut penting.
4. Masukkan konten catatan Anda di area teks.
5. Klik "Save Note" untuk menyimpan catatan Anda.
6. Lihat catatan yang telah disimpan di daftar sebelah kanan.
7. Gunakan bilah pencarian dan filter kategori untuk menemukan catatan tertentu.
8. Klik dua kali pada catatan di daftar untuk melihat detailnya dalam dialog.
