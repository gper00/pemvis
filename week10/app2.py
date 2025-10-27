import sys
import sqlite3
import csv
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QFileDialog, QAbstractItemView, QMenuBar, QAction, QFrame,
    QFormLayout, QSpacerItem, QSizePolicy, QComboBox, QDateEdit
)
from PyQt5.QtCore import Qt, QDate, QSize
from PyQt5.QtGui import QFont, QIcon

DATABASE_NAME = 'movie_manager_v2.db' # Versi database baru

class MovieApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_movie_id = None
        self.genres_list = ["Aksi", "Komedi", "Drama", "Horor", "Sci-Fi", "Romantis", "Thriller", "Animasi", "Dokumenter", "Petualangan", "Fantasi", "Musikal", "Keluarga", "Lainnya"]
        self.init_db()
        self.init_ui()
        self.load_data()
        self.apply_styles()

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
        self.setWindowTitle('Week 10 | Manajer Koleksi Film')
        self.setMinimumSize(QSize(850, 650))
        self.setGeometry(100, 100, 950, 750)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(25, 20, 25, 20)

        self._create_menu_bar()

        user_info_v_layout = QVBoxLayout()
        user_info_v_layout.setSpacing(2)
        self.name_label = QLabel("Nama: UMAM ALPARIZI")
        self.name_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.name_label.setAlignment(Qt.AlignCenter)
        user_info_v_layout.addWidget(self.name_label)
        self.nim_label = QLabel("NIM: F1D02310141")
        self.nim_label.setFont(QFont('Arial', 11))
        self.nim_label.setAlignment(Qt.AlignCenter)
        user_info_v_layout.addWidget(self.nim_label)
        main_layout.addLayout(user_info_v_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        main_layout.addSpacing(10)

        # --- Input Form (QFormLayout dibungkus QHBoxLayout untuk centering) ---
        self.form_layout = QFormLayout()
        self.form_layout.setLabelAlignment(Qt.AlignTrailing) # Label rata kanan
        # self.form_layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop) # Tidak diperlukan lagi, diatur oleh parent QHBoxLayout
        self.form_layout.setHorizontalSpacing(10)
        self.form_layout.setVerticalSpacing(12)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Masukkan judul film")
        # Beri lebar minimum agar tidak terlalu kecil saat QFormLayout menyusut
        self.title_input.setMinimumWidth(250) # Sesuaikan jika perlu
        self.director_input = QLineEdit()
        self.director_input.setPlaceholderText("Masukkan nama sutradara")
        self.director_input.setMinimumWidth(250) # Sesuaikan jika perlu

        self.year_input = QDateEdit()
        self.year_input.setDisplayFormat("yyyy")
        self.year_input.setCalendarPopup(True)
        self.year_input.setDateRange(QDate(1880, 1, 1), QDate.currentDate().addYears(5))
        self.year_input.setDate(QDate.currentDate())
        self.year_input.setMinimumWidth(100) # Agar konsisten

        self.genre_input = QComboBox()
        self.genre_input.addItems(self.genres_list)
        self.genre_input.setMinimumWidth(150) # Agar konsisten

        self.form_layout.addRow(QLabel("Judul Film:"), self.title_input)
        self.form_layout.addRow(QLabel("Sutradara:"), self.director_input)
        self.form_layout.addRow(QLabel("Tahun Rilis:"), self.year_input)
        self.form_layout.addRow(QLabel("Genre:"), self.genre_input)

        # Wadah untuk QFormLayout agar bisa dicentang dengan QHBoxLayout
        form_wrapper_widget = QWidget()
        # Layout ini akan membuat QFormLayout mengambil lebar naturalnya dan terpusat
        centering_layout_for_form = QHBoxLayout(form_wrapper_widget)
        centering_layout_for_form.addStretch(1) # Dorong ke tengah dari kiri
        centering_layout_for_form.addLayout(self.form_layout) # QFormLayout di sini
        centering_layout_for_form.addStretch(1) # Dorong ke tengah dari kanan
        centering_layout_for_form.setContentsMargins(0,0,0,0) # Hapus margin internal jika ada

        # Atur agar form_wrapper_widget tidak terlalu melebar secara keseluruhan
        # Ini akan membatasi seberapa lebar QFormLayout bisa menjadi (termasuk stretch)
        form_wrapper_widget.setMaximumWidth(600) # Atau nilai lain yang sesuai

        main_layout.addWidget(form_wrapper_widget, 0, Qt.AlignHCenter) # Widget pembungkus form di tengah horizontal
        main_layout.addSpacing(5)

        form_buttons_layout = QHBoxLayout()
        form_buttons_layout.setSpacing(10)
        self.save_button = QPushButton("💾 Simpan")
        self.save_button.clicked.connect(self.save_movie)
        self.clear_button = QPushButton("🔄 Bersihkan Form")
        self.clear_button.clicked.connect(self.clear_form_action)
        form_buttons_layout.addStretch()
        form_buttons_layout.addWidget(self.save_button)
        form_buttons_layout.addWidget(self.clear_button)
        form_buttons_layout.addStretch()
        main_layout.addLayout(form_buttons_layout)
        main_layout.addSpacing(15)


        search_layout = QHBoxLayout()
        search_layout.setSpacing(5)
        search_label = QLabel("🔍 Cari Film (Judul/Sutradara/Genre):")
        search_label.setFont(QFont('Arial', 10))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ketik untuk mencari...")
        self.search_input.textChanged.connect(self.search_movies)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Judul", "Sutradara", "Tahun", "Genre"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setHighlightSections(False)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.doubleClicked.connect(self.load_movie_to_form)
        self.table_widget.setAlternatingRowColors(True)
        main_layout.addWidget(self.table_widget)

        table_actions_layout = QHBoxLayout()
        table_actions_layout.setSpacing(10)
        self.delete_button = QPushButton("❌ Hapus Terpilih")
        self.delete_button.clicked.connect(self.delete_movie_action)
        self.export_button = QPushButton("📄 Ekspor ke CSV")
        self.export_button.clicked.connect(self.export_to_csv_action)
        table_actions_layout.addStretch()
        table_actions_layout.addWidget(self.delete_button)
        table_actions_layout.addWidget(self.export_button)
        table_actions_layout.addStretch()
        main_layout.addLayout(table_actions_layout)

        self.clear_form_action()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        export_action = QAction(QIcon.fromTheme("document-save-as"), "Ekspor ke CSV...", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_to_csv_action)
        file_menu.addAction(export_action)
        file_menu.addSeparator()
        exit_action = QAction(QIcon.fromTheme("application-exit"), "&Keluar", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menu_bar.addMenu("&Edit")
        clear_form_action = QAction(QIcon.fromTheme("edit-clear"), "Bersihkan Form Input", self)
        clear_form_action.setShortcut("Ctrl+L")
        clear_form_action.triggered.connect(self.clear_form_action)
        edit_menu.addAction(clear_form_action)
        delete_selected_action = QAction(QIcon.fromTheme("edit-delete"), "Hapus Data Terpilih", self)
        delete_selected_action.setShortcut("Delete") # Qt.Key_Delete bisa lebih baik di beberapa sistem
        delete_selected_action.triggered.connect(self.delete_movie_action)
        edit_menu.addAction(delete_selected_action)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                font-family: Arial, sans-serif;
                background-color: #f4f6f8;
            }
            QLabel {
                font-size: 10pt;
                padding-top: 3px; /* Align with QComboBox/QDateEdit */
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 7px;
                border: 1px solid #ced4da;
                border-radius: 5px;
                font-size: 10pt;
                background-color: #ffffff;
                min-height: 20px; /* Consistent height */
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border-color: #80bdff;
                /* box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25); Consider compatibility */
            }
            QComboBox::drop-down {
                border-left: 1px solid #ced4da;
            }
            QDateEdit::up-button, QDateEdit::down-button {
                width: 20px;
            }
            QPushButton {
                padding: 8px 16px;
                font-size: 10pt;
                font-weight: 500;
                border: 1px solid transparent;
                border-radius: 5px;
                color: white;
                min-height: 22px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QPushButton:pressed {
                opacity: 0.8;
            }
            QTableWidget {
                border: 1px solid #dee2e6;
                gridline-color: #e9ecef;
                font-size: 9pt;
                alternate-background-color: #f8f9fa;
                background-color: white;
                selection-background-color: #b8dffc;
                selection-color: #000;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 7px;
                border: none;
                border-bottom: 1px solid #dee2e6;
                font-weight: bold;
                font-size: 10pt;
                color: #495057;
            }
            QMenuBar {
                background-color: #e0e6ed;
                font-size: 9pt;
                border-bottom: 1px solid #ced4da;
            }
            QMenuBar::item {
                spacing: 4px;
                padding: 5px 12px;
                background: transparent;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background: #cdd5df;
            }
            QMenu {
                background-color: #ffffff;
                border: 1px solid #ced4da;
                font-size: 9pt;
                padding: 5px 0;
            }
            QMenu::item {
                padding: 7px 22px;
            }
            QMenu::item:selected {
                background-color: #007bff;
                color: white;
            }
            QFrame[frameShape="5"] { /* HLine */
                border: none;
                height: 1px;
                background-color: #ced4da;
            }
        """)
        self.name_label.setStyleSheet("font-size: 13pt; font-weight: bold; color: #343a40;")
        self.nim_label.setStyleSheet("font-size: 11pt; color: #495057;")

        self.save_button.setStyleSheet("""
            QPushButton { background-color: #007bff; border-color: #007bff; }
            QPushButton:hover { background-color: #0069d9; border-color: #0062cc; }
            QPushButton:pressed { background-color: #005cbf; border-color: #0056b3; }
        """)
        self.clear_button.setStyleSheet("""
            QPushButton { background-color: #6c757d; border-color: #6c757d; }
            QPushButton:hover { background-color: #5a6268; border-color: #545b62; }
            QPushButton:pressed { background-color: #545b62; border-color: #4e555b; }
        """)
        self.delete_button.setStyleSheet("""
            QPushButton { background-color: #dc3545; border-color: #dc3545; }
            QPushButton:hover { background-color: #c82333; border-color: #bd2130; }
            QPushButton:pressed { background-color: #bd2130; border-color: #b21f2d; }
        """)
        self.export_button.setStyleSheet("""
            QPushButton { background-color: #28a745; border-color: #28a745; }
            QPushButton:hover { background-color: #218838; border-color: #1e7e34; }
            QPushButton:pressed { background-color: #1e7e34; border-color: #1c7430; }
        """)

    def execute_query(self, query, params=()):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        success = False
        try:
            cursor.execute(query, params)
            conn.commit()
            success = True
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Database error: {e} (Query: {query}, Params: {params})")
            QMessageBox.critical(self, "Error Database", f"Terjadi kesalahan database: {e}")
        finally:
            conn.close()
        return success

    def fetch_query(self, query, params=()):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        rows = []
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database fetch error: {e} (Query: {query}, Params: {params})")
            QMessageBox.critical(self, "Error Database", f"Gagal mengambil data: {e}")
        finally:
            conn.close()
        return rows

    def load_data(self):
        movies = self.fetch_query("SELECT id, title, director, year, genre FROM movies ORDER BY title COLLATE NOCASE")
        self.table_widget.setRowCount(0)
        for row_number, movie_data in enumerate(movies):
            self.table_widget.insertRow(row_number)
            movie_id, title, director, year, genre = movie_data

            self.table_widget.setItem(row_number, 0, QTableWidgetItem(str(movie_id)))
            self.table_widget.setItem(row_number, 1, QTableWidgetItem(str(title)))
            self.table_widget.setItem(row_number, 2, QTableWidgetItem(str(director if director else "")))
            self.table_widget.setItem(row_number, 3, QTableWidgetItem(str(year if year else "")))
            self.table_widget.setItem(row_number, 4, QTableWidgetItem(str(genre if genre else "")))

            self.table_widget.item(row_number, 0).setTextAlignment(Qt.AlignCenter)
            if self.table_widget.item(row_number, 3):
                self.table_widget.item(row_number, 3).setTextAlignment(Qt.AlignCenter)


    def save_movie(self):
        title = self.title_input.text().strip()
        director = self.director_input.text().strip()
        year = self.year_input.date().year()
        genre = self.genre_input.currentText()

        if not title:
            QMessageBox.warning(self, "Input Tidak Valid", "Judul film tidak boleh kosong.")
            self.title_input.setFocus()
            return

        query_check = "SELECT id FROM movies WHERE lower(title) = ?"
        params_check = (title.lower(),)
        if self.current_movie_id is not None:
            query_check += " AND id != ?"
            params_check = (title.lower(), self.current_movie_id)

        existing_movies = self.fetch_query(query_check, params_check)
        if existing_movies:
            reply = QMessageBox.question(self, "Konfirmasi Judul Duplikat",
                                         f"Film dengan judul '{title}' sudah ada di database.\nApakah Anda ingin tetap menyimpannya?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return

        if self.current_movie_id is None:
            if self.execute_query(
                "INSERT INTO movies (title, director, year, genre) VALUES (?, ?, ?, ?)",
                (title, director, year, genre)
            ):
                QMessageBox.information(self, "Sukses", f"Film '{title}' berhasil disimpan.")
        else:
            if self.execute_query(
                "UPDATE movies SET title=?, director=?, year=?, genre=? WHERE id=?",
                (title, director, year, genre, self.current_movie_id)
            ):
                QMessageBox.information(self, "Sukses", f"Film '{title}' berhasil diperbarui.")

        self.clear_form_action()
        self.load_data()

    def clear_form_action(self):
        self.current_movie_id = None
        self.title_input.clear()
        self.director_input.clear()
        self.year_input.setDate(QDate.currentDate())
        self.genre_input.setCurrentIndex(0)
        self.save_button.setText("💾 Simpan")
        self.title_input.setFocus()
        self.table_widget.clearSelection()

    def load_movie_to_form(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            return

        selected_row = selected_items[0].row()
        try:
            movie_id = int(self.table_widget.item(selected_row, 0).text())
            title = self.table_widget.item(selected_row, 1).text()
            director = self.table_widget.item(selected_row, 2).text()
            year_str = self.table_widget.item(selected_row, 3).text()
            genre = self.table_widget.item(selected_row, 4).text()

            self.current_movie_id = movie_id
            self.title_input.setText(title)
            self.director_input.setText(director if director != "None" else "")

            if year_str and year_str.isdigit():
                self.year_input.setDate(QDate(int(year_str), 1, 1))
            else:
                self.year_input.setDate(QDate.currentDate())

            genre_index = self.genre_input.findText(genre, Qt.MatchFixedString)
            if genre_index >= 0:
                self.genre_input.setCurrentIndex(genre_index)
            else:
                default_genre = "Lainnya"
                if default_genre in self.genres_list:
                     self.genre_input.setCurrentIndex(self.genres_list.index(default_genre))
                elif self.genres_list: # Fallback to first item if "Lainnya" not present
                    self.genre_input.setCurrentIndex(0)


            self.save_button.setText("💾 Perbarui Data")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data film ke form: {e}")
            self.clear_form_action()


    def delete_movie_action(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Tidak Ada Pilihan", "Pilih film yang ingin dihapus dari tabel.")
            return

        selected_row = selected_items[0].row()
        movie_id_item = self.table_widget.item(selected_row, 0)
        movie_title_item = self.table_widget.item(selected_row, 1)

        if not movie_id_item or not movie_title_item:
            QMessageBox.warning(self, "Error", "Data baris tidak lengkap untuk dihapus.")
            return

        movie_id = movie_id_item.text()
        movie_title = movie_title_item.text()


        reply = QMessageBox.question(self, "Konfirmasi Hapus",
                                     f"Apakah Anda yakin ingin menghapus film '{movie_title}' (ID: {movie_id})?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.execute_query("DELETE FROM movies WHERE id=?", (movie_id,)):
                QMessageBox.information(self, "Sukses", f"Film '{movie_title}' berhasil dihapus.")
                self.load_data()
                try:
                    if self.current_movie_id == int(movie_id):
                        self.clear_form_action()
                except ValueError: # Jika movie_id tidak bisa di-cast ke int (seharusnya tidak terjadi)
                    self.clear_form_action()


    def search_movies(self):
        search_text = self.search_input.text().lower().strip()
        for i in range(self.table_widget.rowCount()):
            title_item = self.table_widget.item(i, 1)
            director_item = self.table_widget.item(i, 2)
            genre_item = self.table_widget.item(i, 4)

            title_match = title_item and search_text in title_item.text().lower()
            director_match = director_item and search_text in director_item.text().lower()
            genre_match = genre_item and search_text in genre_item.text().lower()

            self.table_widget.setRowHidden(i, not (title_match or director_match or genre_match))

    def export_to_csv_action(self):
        if self.table_widget.rowCount() == 0:
            QMessageBox.information(self, "Data Kosong", "Tidak ada data untuk diekspor.")
            return

        default_filename = f"koleksi_film_UMAM_F1D02310141_{QDate.currentDate().toString('yyyyMMdd')}.csv"
        path, _ = QFileDialog.getSaveFileName(self, "Ekspor Data ke CSV", default_filename,
                                              "CSV Files (*.csv);;All Files (*)")
        if path:
            try:
                with open(path, 'w', newline='', encoding='utf-8-sig') as csvfile: # utf-8-sig untuk Excel compatibility
                    writer = csv.writer(csvfile, delimiter=';') # Sesuai standar Indonesia, Excel lebih suka ;
                    headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]
                    writer.writerow(headers)
                    for row in range(self.table_widget.rowCount()):
                        if not self.table_widget.isRowHidden(row):
                            row_data = [self.table_widget.item(row, col).text() if self.table_widget.item(row, col) else ''
                                        for col in range(self.table_widget.columnCount())]
                            writer.writerow(row_data)
                QMessageBox.information(self, "Ekspor Berhasil", f"Data berhasil diekspor ke:\n{path}")
            except Exception as e:
                QMessageBox.critical(self, "Error Ekspor", f"Gagal mengekspor data: {e}\nPeriksa apakah file sedang terbuka.")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Konfirmasi Keluar',
                                     "Apakah Anda yakin ingin keluar dari aplikasi?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Coba atur nama tema ikon secara eksplisit jika ikon standar tidak muncul
    # QIcon.setThemeName("breeze") # Contoh untuk KDE, atau "Adwaita" untuk GNOME, dll.
    # Atau gunakan fallback jika tema tidak ditemukan
    # if not QIcon.hasThemeIcon("document-save-as"):
    #     QIcon.setThemeName("gnome") # Fallback umum
    # if not QIcon.hasThemeIcon("document-save-as"):
    #     print("Peringatan: Ikon tema standar tidak ditemukan. Coba instal paket ikon atau atur tema ikon.")
    window = MovieApp()
    window.show()
    sys.exit(app.exec_())
