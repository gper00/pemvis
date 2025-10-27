import sys
import sqlite3
import csv
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QFileDialog, QAbstractItemView, QMenuBar, QAction, QFrame,
    QFormLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon # QIcon ditambahkan jika ingin ikon pada action

DATABASE_NAME = 'movie_manager.db' # Nama database baru untuk menghindari konflik jika ada versi lama

class MovieApp(QMainWindow): # Mengubah QWidget menjadi QMainWindow
    def __init__(self):
        super().__init__()
        self.current_movie_id = None
        self.init_db()
        self.init_ui()
        self.load_data()
        self.apply_styles() # Menerapkan stylesheet

    def init_db(self):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                director TEXT,
                year INTEGER,
                genre TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def init_ui(self):
        self.setWindowTitle('Week 10 - Manajer Koleksi Film')
        self.setGeometry(100, 100, 1000, 800) # Sedikit lebih besar

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout untuk Central Widget
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # --- Menu Bar ---
        self._create_menu_bar()

        # --- Informasi Pengguna ---
        user_info_v_layout = QVBoxLayout()
        user_info_v_layout.setSpacing(2) # Jarak antar label nama dan NIM

        self.name_label = QLabel("Nama: UMAM ALPARIZI")
        self.name_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.name_label.setAlignment(Qt.AlignCenter)
        user_info_v_layout.addWidget(self.name_label)

        self.nim_label = QLabel("NIM: F1D02310141")
        self.nim_label.setFont(QFont('Arial', 11))
        self.nim_label.setAlignment(Qt.AlignCenter)
        user_info_v_layout.addWidget(self.nim_label)

        main_layout.addLayout(user_info_v_layout)

        # Garis Pemisah
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setFixedHeight(2)
        line.setStyleSheet("background-color: #c0c0c0;")
        main_layout.addWidget(line)
        main_layout.addSpacing(10)

        # --- Input Form ---
        form_container_widget = QWidget()
        form_container_layout = QVBoxLayout(form_container_widget)
        form_container_layout.setContentsMargins(0,0,0,0)
        form_container_layout.setSpacing(10)  # Spacing between fields

        # Create input fields
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Masukkan judul film")
        self.director_input = QLineEdit()
        self.director_input.setPlaceholderText("Masukkan nama sutradara")
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Contoh: 2023")
        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Contoh: Aksi, Komedi")

        # Helper function to create form rows
        def create_form_row(label_text, input_widget):
            row_layout = QHBoxLayout()

            # Create container widget for consistent width
            container = QWidget()
            container.setFixedWidth(600)  # Total width dikurangi
            container_layout = QHBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(15)  # Space between label and input

            label = QLabel(label_text)
            label.setFixedWidth(180)  # ~3/12 of container width
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            input_widget.setFixedWidth(400)  # ~8/12 of container width

            container_layout.addWidget(label)
            container_layout.addWidget(input_widget)

            row_layout.addWidget(container)
            row_layout.setAlignment(Qt.AlignCenter)
            return row_layout

        # Add form rows
        form_container_layout.addLayout(create_form_row("Judul Film:", self.title_input))
        form_container_layout.addLayout(create_form_row("Sutradara:", self.director_input))
        form_container_layout.addLayout(create_form_row("Tahun Rilis:", self.year_input))
        form_container_layout.addLayout(create_form_row("Genre:", self.genre_input))

        # Add buttons
        form_buttons_layout = QHBoxLayout()
        form_buttons_layout.setSpacing(10)
        self.save_button = QPushButton("💾 Simpan")
        self.save_button.clicked.connect(self.save_movie)
        self.clear_button = QPushButton("🔄 Bersihkan Form")
        self.clear_button.clicked.connect(self.clear_form_action)

        # Create container for buttons with same alignment as form fields
        buttons_container = QWidget()
        buttons_container.setFixedWidth(600)  # Same as form container
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(180, 0, 0, 0)  # Matches exactly with input start position
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addStretch()

        form_buttons_layout.addWidget(buttons_container)
        form_buttons_layout.setAlignment(Qt.AlignCenter)

        form_container_layout.addSpacing(15)
        form_container_layout.addLayout(form_buttons_layout)
        main_layout.addWidget(form_container_widget)
        main_layout.addSpacing(10)

        # --- Pencarian ---
        search_layout = QHBoxLayout()
        search_layout.setSpacing(5)
        search_label = QLabel("🔍 Cari Film:")
        search_label.setFont(QFont('Arial', 10))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ketik judul untuk mencari...")
        self.search_input.textChanged.connect(self.search_movies)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # --- Tabel Data ---
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Judul", "Sutradara", "Tahun", "Genre"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setHighlightSections(False) # Biar tidak ada highlight aneh saat diklik
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.doubleClicked.connect(self.load_movie_to_form)
        self.table_widget.setAlternatingRowColors(True) # Warna baris selang-seling
        main_layout.addWidget(self.table_widget)

        # --- Tombol Aksi Tabel (Delete, Export) ---
        table_actions_layout = QHBoxLayout()
        table_actions_layout.setSpacing(10)
        self.delete_button = QPushButton("❌ Hapus Data Terpilih")
        self.delete_button.clicked.connect(self.delete_movie_action) # Ubah ke action
        self.export_button = QPushButton("📄 Ekspor ke CSV")
        self.export_button.clicked.connect(self.export_to_csv_action) # Ubah ke action

        table_actions_layout.addStretch()
        table_actions_layout.addWidget(self.delete_button)
        table_actions_layout.addWidget(self.export_button)
        table_actions_layout.addStretch()
        main_layout.addLayout(table_actions_layout)

        self.clear_form_action() # Panggil untuk inisialisasi state tombol simpan

    def _create_menu_bar(self):
        menu_bar = self.menuBar() # QMainWindow sudah punya menuBar()

        # Menu File
        file_menu = menu_bar.addMenu("&File")

        export_action = QAction("Ekspor ke CSV...", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_to_csv_action)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("&Keluar", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close) # self.close() adalah slot bawaan QMainWindow
        file_menu.addAction(exit_action)

        # Menu Edit
        edit_menu = menu_bar.addMenu("&Edit")

        clear_form_action = QAction("Bersihkan Form Input", self)
        clear_form_action.setShortcut("Ctrl+L")
        clear_form_action.triggered.connect(self.clear_form_action)
        edit_menu.addAction(clear_form_action)

        delete_selected_action = QAction("Hapus Data Terpilih", self)
        delete_selected_action.setShortcut("Delete") # Tombol Delete keyboard
        delete_selected_action.triggered.connect(self.delete_movie_action)
        edit_menu.addAction(delete_selected_action)

    def apply_styles(self):
        """Menerapkan QSS untuk styling."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0; /* Warna latar belakang utama */
            }
            QWidget { /* Berlaku untuk central widget dan lainnya jika tidak dioverride */
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 10pt;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 10pt;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 1px solid #0078d7; /* Warna border saat fokus */
            }
            QPushButton {
                padding: 8px 15px;
                font-size: 10pt;
                border: 1px solid #0078d7;
                border-radius: 4px;
                background-color: #0078d7; /* Biru primer */
                color: white;
            }
            QPushButton:hover {
                background-color: #005a9e; /* Biru lebih gelap saat hover */
            }
            QPushButton:pressed {
                background-color: #004c8a; /* Biru sangat gelap saat ditekan */
            }
            QTableWidget {
                border: 1px solid #ddd;
                gridline-color: #e0e0e0;
                font-size: 9pt;
                alternate-background-color: #f9f9f9; /* Untuk alternatingRowColors */
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #e9ecef; /* Warna header tabel */
                padding: 6px;
                border: none;
                border-bottom: 1px solid #ddd;
                font-weight: bold;
                font-size: 10pt;
            }
            QMenuBar {
                background-color: #e0e0e0;
                font-size: 9pt;
            }
            QMenuBar::item {
                spacing: 3px;
                padding: 4px 10px;
                background: transparent;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background: #c0c0c0;
            }
            QMenu {
                background-color: #f8f8f8;
                border: 1px solid #bbb;
                font-size: 9pt;
            }
            QMenu::item {
                padding: 5px 20px 5px 20px;
            }
            QMenu::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QFrame[frameShape="5"] { /* Styling untuk QFrame.HLine */
                color: #c0c0c0;
            }
        """)
        # Styling khusus untuk tombol clear agar berbeda
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d; /* Abu-abu */
                border-color: #6c757d;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
            }
        """)
        # Styling khusus untuk tombol delete agar berbeda
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545; /* Merah */
                border-color: #dc3545;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        # Styling khusus untuk tombol export
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745; /* Hijau */
                border-color: #28a745;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        # Menyesuaikan ukuran font label identitas
        self.name_label.setStyleSheet("font-size: 13pt; font-weight: bold; color: #333;")
        self.nim_label.setStyleSheet("font-size: 11pt; color: #555;")


    def execute_query(self, query, params=()):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
        except Exception as e:
            conn.rollback() # Rollback jika terjadi error
            print(f"Database error: {e}") # Logging error ke konsol
            QMessageBox.critical(self, "Error Database", f"Terjadi kesalahan database: {e}")
        finally:
            conn.close()
        return cursor

    def fetch_query(self, query, params=()):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        rows = []
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
        except Exception as e:
            print(f"Database fetch error: {e}")
            QMessageBox.critical(self, "Error Database", f"Gagal mengambil data: {e}")
        finally:
            conn.close()
        return rows

    def load_data(self):
        movies = self.fetch_query("SELECT id, title, director, year, genre FROM movies ORDER BY title COLLATE NOCASE")
        self.table_widget.setRowCount(0)
        for row_number, movie in enumerate(movies):
            self.table_widget.insertRow(row_number)
            for column_number, data in enumerate(movie):
                item = QTableWidgetItem(str(data) if data is not None else "")
                # ID (kolom 0) rata tengah dan non-editable
                if column_number == 0:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(row_number, column_number, item)
        # self.table_widget.resizeColumnsToContents() # Diatur oleh Stretch
        # self.table_widget.resizeRowsToContents()


    def save_movie(self):
        title = self.title_input.text().strip()
        director = self.director_input.text().strip()
        year_text = self.year_input.text().strip()
        genre = self.genre_input.text().strip()

        if not title:
            QMessageBox.warning(self, "Input Tidak Valid", "Judul film tidak boleh kosong.")
            self.title_input.setFocus()
            return

        year = None
        if year_text:
            try:
                year_val = int(year_text)
                if 1800 <= year_val <= 2100: # Validasi tahun
                    year = year_val
                else:
                    QMessageBox.warning(self, "Input Tidak Valid", "Tahun rilis tidak valid (antara 1800-2100).")
                    self.year_input.setFocus()
                    return
            except ValueError:
                QMessageBox.warning(self, "Input Tidak Valid", "Tahun rilis harus berupa angka.")
                self.year_input.setFocus()
                return

        # Konfirmasi sebelum menyimpan jika ada data dengan judul yang sama (kecuali sedang update ID yang sama)
        existing_movies_with_same_title = self.fetch_query("SELECT id, title FROM movies WHERE lower(title) = ?", (title.lower(),))
        is_updating_self = False
        if self.current_movie_id is not None:
            for movie_id, _ in existing_movies_with_same_title:
                if movie_id == self.current_movie_id:
                    is_updating_self = True
                    break

        if existing_movies_with_same_title and not is_updating_self and (self.current_movie_id is None or not any(m[0] == self.current_movie_id for m in existing_movies_with_same_title)):
             reply = QMessageBox.question(self, "Konfirmasi Judul Duplikat",
                                     f"Film dengan judul '{title}' sudah ada. Tetap simpan?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
             if reply == QMessageBox.No:
                 return


        if self.current_movie_id is None:
            self.execute_query(
                "INSERT INTO movies (title, director, year, genre) VALUES (?, ?, ?, ?)",
                (title, director, year, genre)
            )
            QMessageBox.information(self, "Sukses", f"Film '{title}' berhasil disimpan.")
        else:
            self.execute_query(
                "UPDATE movies SET title=?, director=?, year=?, genre=? WHERE id=?",
                (title, director, year, genre, self.current_movie_id)
            )
            QMessageBox.information(self, "Sukses", f"Film '{title}' berhasil diperbarui.")

        self.clear_form_action() # Reset form
        self.load_data()

    def clear_form_action(self): # Diubah nama agar jelas ini adalah 'action'
        self.current_movie_id = None
        self.title_input.clear()
        self.director_input.clear()
        self.year_input.clear()
        self.genre_input.clear()
        self.save_button.setText("💾 Simpan")
        self.save_button.setIcon(QIcon()) # Reset ikon jika ada
        self.title_input.setFocus()
        self.table_widget.clearSelection() # Hapus seleksi di tabel

    def load_movie_to_form(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            return

        selected_row = selected_items[0].row()
        try:
            movie_id = int(self.table_widget.item(selected_row, 0).text())
            title = self.table_widget.item(selected_row, 1).text()
            director = self.table_widget.item(selected_row, 2).text()
            year = self.table_widget.item(selected_row, 3).text()
            genre = self.table_widget.item(selected_row, 4).text()

            self.current_movie_id = movie_id
            self.title_input.setText(title)
            self.director_input.setText(director)
            self.year_input.setText(year if year != "None" else "")
            self.genre_input.setText(genre if genre != "None" else "")
            self.save_button.setText("💾 Perbarui Data")
            # Anda bisa menambahkan ikon untuk tombol update jika diinginkan
            # self.save_button.setIcon(QIcon("path/to/update_icon.png"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data film ke form: {e}")
            self.clear_form_action()


    def delete_movie_action(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Tidak Ada Pilihan", "Pilih film yang ingin dihapus dari tabel.")
            return

        selected_row = selected_items[0].row() # Ambil baris dari item pertama yang terpilih
        movie_id = self.table_widget.item(selected_row, 0).text()
        movie_title = self.table_widget.item(selected_row, 1).text()

        reply = QMessageBox.question(self, "Konfirmasi Hapus",
                                     f"Apakah Anda yakin ingin menghapus film '{movie_title}' (ID: {movie_id})?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.execute_query("DELETE FROM movies WHERE id=?", (movie_id,))
            QMessageBox.information(self, "Sukses", f"Film '{movie_title}' berhasil dihapus.")
            self.load_data()
            # Jika film yang sedang di-edit dihapus, bersihkan form
            if self.current_movie_id == int(movie_id):
                self.clear_form_action()

    def search_movies(self):
        search_text = self.search_input.text().lower().strip()
        for i in range(self.table_widget.rowCount()):
            title_item = self.table_widget.item(i, 1) # Kolom judul
            director_item = self.table_widget.item(i, 2) # Kolom sutradara
            genre_item = self.table_widget.item(i, 4) # Kolom genre

            # Pastikan item tidak None sebelum memanggil .text()
            title_match = title_item and search_text in title_item.text().lower()
            director_match = director_item and search_text in director_item.text().lower()
            genre_match = genre_item and search_text in genre_item.text().lower()

            if title_match or director_match or genre_match:
                self.table_widget.setRowHidden(i, False)
            else:
                self.table_widget.setRowHidden(i, True)

    def export_to_csv_action(self):
        if self.table_widget.rowCount() == 0:
            QMessageBox.information(self, "Data Kosong", "Tidak ada data untuk diekspor.")
            return

        default_filename = "koleksi_film_UMAM_F1D02310141.csv"
        path, _ = QFileDialog.getSaveFileName(self, "Ekspor Data ke CSV", default_filename,
                                              "CSV Files (*.csv);;All Files (*)")
        if path:
            try:
                with open(path, 'w', newline='', encoding='utf-8-sig') as csvfile: # utf-8-sig untuk Excel
                    writer = csv.writer(csvfile, delimiter=';') # Menggunakan semicolon sebagai delimiter
                    headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]
                    writer.writerow(headers)

                    for row in range(self.table_widget.rowCount()):
                        if not self.table_widget.isRowHidden(row):
                            row_data = []
                            for column in range(self.table_widget.columnCount()):
                                item = self.table_widget.item(row, column)
                                row_data.append(item.text() if item else '')
                            writer.writerow(row_data)
                QMessageBox.information(self, "Ekspor Berhasil", f"Data berhasil diekspor ke:\n{path}")
            except Exception as e:
                QMessageBox.critical(self, "Error Ekspor", f"Gagal mengekspor data: {e}")

    def closeEvent(self, event):
        """Menangani event penutupan jendela."""
        reply = QMessageBox.question(self, 'Konfirmasi Keluar',
                                     "Apakah Anda yakin ingin keluar dari aplikasi?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyle('Fusion') # Fusion style bisa jadi alternatif jika QSS tidak terlalu kompleks
    window = MovieApp()
    window.show()
    sys.exit(app.exec_())
