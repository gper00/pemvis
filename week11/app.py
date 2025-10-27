import sys
import sqlite3
import csv
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QFileDialog, QAbstractItemView, QMenuBar, QAction, QFrame,
    QFormLayout, QSpacerItem, QSizePolicy, QDockWidget, QStatusBar, # QScrollArea dihapus dari sini jika tidak dipakai lagi
    QTextEdit # QScrollArea tetap diimpor jika masih ada penggunaan lain (tidak dalam kasus ini)
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QClipboard

DATABASE_NAME = 'movies.db' # Versi database naik lagi

class MovieApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_movie_id = None
        self.init_db()
        self.init_ui()
        self.load_data() # load_data akan memanggil _update_data_count_status
        self.apply_styles()
        self._update_status_message("Aplikasi siap.")

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
        self.setWindowTitle('Week 11 - Manajer Koleksi Film (Revisi)')
        self.setGeometry(100, 100, 1100, 750) # Ukuran disesuaikan sedikit

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout untuk Central Widget
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10) # Mengurangi spacing sedikit
        main_layout.setContentsMargins(10, 10, 10, 10)

        self._create_menu_bar()
        self._create_status_bar()

        user_info_v_layout = QVBoxLayout()
        user_info_v_layout.setSpacing(2)
        app_title_label = QLabel("Manajer Koleksi Film")
        app_title_label.setFont(QFont('Arial', 15, QFont.Bold)) # Sedikit lebih kecil
        app_title_label.setAlignment(Qt.AlignCenter)
        user_info_v_layout.addWidget(app_title_label)
        self.name_label_top = QLabel("Oleh: UMAM ALPARIZI")
        self.name_label_top.setFont(QFont('Arial', 9)) # Sedikit lebih kecil
        self.name_label_top.setAlignment(Qt.AlignCenter)
        user_info_v_layout.addWidget(self.name_label_top)
        main_layout.addLayout(user_info_v_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setFixedHeight(1) # Lebih tipis
        main_layout.addWidget(line)
        main_layout.addSpacing(5) # Mengurangi spacing

        # --- Input Form Area (TIDAK LAGI dibungkus QScrollArea) ---
        self.form_container_widget = QWidget() # Widget yang berisi form

        form_container_layout = QVBoxLayout(self.form_container_widget)
        form_container_layout.setContentsMargins(5,5,5,5)
        form_container_layout.setSpacing(8)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Masukkan judul film")
        self.director_input = QLineEdit()
        self.director_input.setPlaceholderText("Masukkan nama sutradara")
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Contoh: 2023")
        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Contoh: Aksi, Komedi")

        self.paste_button = QPushButton("Tempel")
        self.paste_button.setIcon(QIcon.fromTheme("edit-paste"))
        self.paste_button.setToolTip("Tempel dari Papan Klip (Ctrl+V)")
        self.paste_button.clicked.connect(self.paste_title_from_clipboard)
        self.paste_button.setFixedWidth(75)

        def create_form_row(label_text, input_widget, action_widget=None):
            row_layout = QHBoxLayout()
            # row_layout.setSpacing(0) # Dihapus, biarkan default atau atur di parent

            # Container untuk menjaga alignment jika window lebih lebar dari form
            form_align_container = QWidget()
            form_align_layout = QHBoxLayout(form_align_container)
            form_align_layout.setContentsMargins(0,0,0,0)
            form_align_layout.setSpacing(10)


            label = QLabel(label_text)
            label.setFixedWidth(100) # Lebar label disesuaikan
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            input_container_layout = QHBoxLayout()
            input_container_layout.setContentsMargins(0,0,0,0)
            input_container_layout.setSpacing(5)
            input_container_layout.addWidget(input_widget, 1)
            if action_widget:
                input_container_layout.addWidget(action_widget)

            form_align_layout.addWidget(label)
            form_align_layout.addLayout(input_container_layout)

            # Untuk membatasi lebar form dan memusatkannya
            # row_layout.addStretch() # Tambahkan stretch di kiri
            row_layout.addWidget(form_align_container) # Kontainer utama form
            # row_layout.addStretch() # Tambahkan stretch di kanan
            row_layout.setAlignment(Qt.AlignCenter) # Pastikan row terpusat

            return row_layout

        form_container_layout.addLayout(create_form_row("Judul Film:", self.title_input, self.paste_button))
        form_container_layout.addLayout(create_form_row("Sutradara:", self.director_input))
        form_container_layout.addLayout(create_form_row("Tahun Rilis:", self.year_input))
        form_container_layout.addLayout(create_form_row("Genre:", self.genre_input))

        form_buttons_layout = QHBoxLayout()
        form_buttons_layout.setSpacing(10)
        self.save_button = QPushButton("💾 Simpan")
        self.save_button.clicked.connect(self.save_movie)
        self.clear_button = QPushButton("🔄 Bersihkan") # Teks dipersingkat
        self.clear_button.clicked.connect(self.clear_form_action)

        # Container untuk tombol agar align dengan input field
        buttons_container_align = QWidget()
        buttons_layout_inner = QHBoxLayout(buttons_container_align)
        buttons_layout_inner.setContentsMargins(100 + 10, 0, 0, 0) # (lebar_label + spacing_antar_label_input)
        buttons_layout_inner.setSpacing(10)
        buttons_layout_inner.addWidget(self.save_button)
        buttons_layout_inner.addWidget(self.clear_button)
        buttons_layout_inner.addStretch() # Dorong tombol ke kiri dalam containernya

        form_buttons_layout.addWidget(buttons_container_align)
        form_buttons_layout.setAlignment(Qt.AlignCenter) # Pusatkan seluruh baris tombol

        form_container_layout.addSpacing(10)
        form_container_layout.addLayout(form_buttons_layout)

        # Menambahkan form_container_widget langsung ke main_layout
        # self.form_container_widget memiliki size policy default (Preferred),
        # yang membuatnya mengambil ruang yang dibutuhkan.
        main_layout.addWidget(self.form_container_widget)


        # --- Tabel Data ---
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Judul", "Sutradara", "Tahun", "Genre"])

        # Pengaturan scrollbar tabel:
        # Scrollbar vertikal akan muncul otomatis jika baris data banyak.
        # Scrollbar horizontal akan muncul jika total lebar kolom melebihi lebar widget tabel.
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.setWordWrap(False) # Penting untuk horizontal scrolling jika data panjang

        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive) # Izinkan pengguna mengubah ukuran kolom
        header.setStretchLastSection(False) # Jangan paksakan kolom terakhir mengisi sisa
        # Set lebar awal yang masuk akal, pengguna bisa resize
        self.table_widget.setColumnWidth(0, 50)  # ID
        self.table_widget.setColumnWidth(1, 250) # Judul
        self.table_widget.setColumnWidth(2, 200) # Sutradara
        self.table_widget.setColumnWidth(3, 80)  # Tahun
        self.table_widget.setColumnWidth(4, 150) # Genre
        # Jika ingin beberapa kolom tetap stretch:
        # header.setSectionResizeMode(1, QHeaderView.Stretch) # Judul
        # header.setSectionResizeMode(2, QHeaderView.Stretch) # Sutradara

        self.table_widget.horizontalHeader().setHighlightSections(False)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.doubleClicked.connect(self.load_movie_to_form)
        self.table_widget.setAlternatingRowColors(True)
        main_layout.addWidget(self.table_widget, 1) # Stretch factor 1, agar bisa membesar

        table_actions_layout = QHBoxLayout()
        table_actions_layout.setSpacing(10)
        self.delete_button = QPushButton("❌ Hapus Terpilih") # Teks dipersingkat
        self.delete_button.clicked.connect(self.delete_movie_action)
        self.export_button = QPushButton("📄 Ekspor CSV") # Teks dipersingkat
        self.export_button.clicked.connect(self.export_to_csv_action)

        table_actions_layout.addStretch()
        table_actions_layout.addWidget(self.delete_button)
        table_actions_layout.addWidget(self.export_button)
        table_actions_layout.addStretch()
        main_layout.addLayout(table_actions_layout)

        self._create_dock_widgets()
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
        clear_form_action = QAction(QIcon.fromTheme("edit-clear"), "Bersihkan Form", self)
        clear_form_action.setShortcut("Ctrl+L")
        clear_form_action.triggered.connect(self.clear_form_action)
        edit_menu.addAction(clear_form_action)
        delete_selected_action = QAction(QIcon.fromTheme("edit-delete"), "Hapus Terpilih", self)
        delete_selected_action.setShortcut("Delete")
        delete_selected_action.triggered.connect(self.delete_movie_action)
        edit_menu.addAction(delete_selected_action)

        view_menu = menu_bar.addMenu("&Tampilan")
        self.toggle_search_dock_action = QAction("Panel Pencarian", self, checkable=True)
        self.toggle_search_dock_action.setChecked(True)
        self.toggle_search_dock_action.triggered.connect(self.toggle_search_dock)
        view_menu.addAction(self.toggle_search_dock_action)
        self.toggle_help_dock_action = QAction("Panel Bantuan", self, checkable=True)
        self.toggle_help_dock_action.setChecked(True)
        self.toggle_help_dock_action.triggered.connect(self.toggle_help_dock)
        view_menu.addAction(self.toggle_help_dock_action)

    def _create_status_bar(self):
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("QStatusBar::item { border: none; }")

        self.status_message_label = QLabel("Siap.") # Untuk pesan umum
        self.status_message_label.setFont(QFont("Arial", 9))
        self.status_message_label.setContentsMargins(5,0,5,0)

        self.status_data_count_label = QLabel("Data: 0") # Untuk jumlah data
        self.status_data_count_label.setFont(QFont("Arial", 9))
        self.status_data_count_label.setContentsMargins(5,0,15,0) # Margin kanan lebih besar

        self.status_name_label = QLabel("UMAM ALPARIZI")
        self.status_name_label.setFont(QFont("Arial", 9))
        self.status_name_label.setToolTip("Nama Pengembang Aplikasi")
        self.status_name_label.setContentsMargins(5,0,5,0)

        self.status_nim_label = QLabel("NIM: F1D02310141")
        self.status_nim_label.setFont(QFont("Arial", 9))
        self.status_nim_label.setToolTip("Nomor Induk Mahasiswa")
        self.status_nim_label.setContentsMargins(5,0,5,0)

        self.status_bar.addWidget(self.status_message_label, 1) # Stretch factor 1
        self.status_bar.addWidget(self.status_data_count_label) # Ukuran sesuai konten
        self.status_bar.addPermanentWidget(self.status_name_label)
        self.status_bar.addPermanentWidget(self.status_nim_label)

    def _update_status_message(self, message):
        if hasattr(self, 'status_message_label'):
            self.status_message_label.setText(message)

    def _update_data_count_status(self, count):
        if hasattr(self, 'status_data_count_label'):
            self.status_data_count_label.setText(f"Data: {count}")


    def _create_dock_widgets(self):
        self.search_dock_widget = QDockWidget("Panel Pencarian", self)
        self.search_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        search_widget_content = QWidget()
        search_layout_dock = QVBoxLayout(search_widget_content)
        search_layout_dock.setContentsMargins(10,10,10,10)
        search_layout_dock.setSpacing(5)
        search_label = QLabel("🔍 Cari Film (Judul, Sutradara, Genre):")
        search_label.setFont(QFont('Arial', 10))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ketik untuk mencari...")
        self.search_input.textChanged.connect(self.search_movies)
        search_layout_dock.addWidget(search_label)
        search_layout_dock.addWidget(self.search_input)
        search_layout_dock.addStretch()
        self.search_dock_widget.setWidget(search_widget_content)
        self.addDockWidget(Qt.RightDockWidgetArea, self.search_dock_widget)
        self.search_dock_widget.visibilityChanged.connect(self.toggle_search_dock_action.setChecked)

        self.help_dock_widget = QDockWidget("Panel Bantuan", self)
        self.help_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        help_content_widget = QWidget()
        help_layout = QVBoxLayout(help_content_widget)
        help_layout.setContentsMargins(10,10,10,10)
        help_text_edit = QTextEdit()
        help_text_edit.setReadOnly(True)
        help_text_edit.setHtml("""
            <h3>Panduan Penggunaan Aplikasi Manajer Film</h3>
            <p>Aplikasi ini memungkinkan Anda untuk mengelola koleksi film pribadi Anda.</p>
            <h4>Fitur Utama:</h4>
            <ul>
                <li><b>Menambah Film:</b> Isi detail film pada formulir dan klik "Simpan".</li>
                <li><b>Memperbarui Film:</b> Klik dua kali pada data film di tabel, ubah detail di formulir, lalu klik "Perbarui Data".</li>
                <li><b>Menghapus Film:</b> Pilih film dari tabel dan klik "Hapus Terpilih" atau tekan tombol Delete.</li>
                <li><b>Mencari Film:</b> Gunakan panel pencarian untuk filter film berdasarkan judul, sutradara, atau genre.</li>
                <li><b>Ekspor Data:</b> Simpan koleksi film Anda ke file CSV melalui menu File atau tombol "Ekspor CSV".</li>
                <li><b>Tempel Judul:</b> Gunakan tombol "Tempel" di sebelah field judul untuk menempel teks dari clipboard.</li>
            </ul>
            <h4>Panel Tambahan:</h4>
            <p>Anda dapat menampilkan/menyembunyikan panel Pencarian dan Bantuan melalui menu "Tampilan". Panel ini juga bisa dilepas (float) dan dipindahkan ke area lain.</p>
            <hr>
            <p><b>Pengembang:</b> UMAM ALPARIZI</p>
            <p><b>NIM:</b> F1D02310141</p>
        """)
        help_layout.addWidget(help_text_edit)
        self.help_dock_widget.setWidget(help_content_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.help_dock_widget)
        self.help_dock_widget.visibilityChanged.connect(self.toggle_help_dock_action.setChecked)

    def toggle_search_dock(self, checked):
        self.search_dock_widget.setVisible(checked)

    def toggle_help_dock(self, checked):
        self.help_dock_widget.setVisible(checked)

    def paste_title_from_clipboard(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            self.title_input.setText(text)
            self._update_status_message(f"Judul '{text[:30]}...' ditempel.")
        else:
            self._update_status_message("Clipboard kosong.")

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f4f4f4; }
            QWidget { font-family: Segoe UI, Arial, sans-serif; } /* Font lebih modern */
            QLabel { font-size: 9pt; } /* Ukuran font default label */
            QLineEdit {
                padding: 6px; border: 1px solid #ccc; border-radius: 3px;
                font-size: 9pt; background-color: #ffffff;
            }
            QLineEdit:focus { border: 1px solid #0078d7; }
            QPushButton {
                padding: 6px 10px; font-size: 9pt; border-radius: 3px;
                background-color: #0078d7; color: white;
                border: 1px solid #0078d7; /* Border konsisten */
                min-height: 18px;
            }
            QPushButton:hover { background-color: #005a9e; border-color: #005393;}
            QPushButton:pressed { background-color: #004c8a; border-color: #00457c;}
            QTableWidget {
                border: 1px solid #ddd; gridline-color: #e0e0e0; font-size: 9pt;
                alternate-background-color: #f9f9f9; background-color: white;
            }
            QTableWidget::item { padding: 4px; } /* Padding item tabel lebih kecil */
            QHeaderView::section {
                background-color: #e9ecef; padding: 5px; border: none;
                border-bottom: 1px solid #ddd; font-weight: bold; font-size: 9pt;
            }
            QMenuBar { background-color: #e0e0e0; font-size: 9pt; }
            QMenuBar::item { padding: 4px 8px; background: transparent; border-radius: 3px; }
            QMenuBar::item:selected { background: #c0c0c0; }
            QMenu { background-color: #f8f8f8; border: 1px solid #bbb; font-size: 9pt; }
            QMenu::item { padding: 4px 18px; }
            QMenu::item:selected { background-color: #0078d7; color: white; }
            QFrame[frameShape="5"] { color: #d0d0d0; } /* HLine lebih terang */
            QDockWidget { font-weight: bold; font-size: 10pt; }
            QDockWidget::title {
                text-align: left; background: #e0e0e0; padding: 6px;
                border: 1px solid #c0c0c0; border-bottom: 1px solid #b0b0b0; /* Border title dock */
            }
            QStatusBar { font-size: 9pt; }
            QStatusBar QLabel { padding: 1px 3px; border: none; }
        """)
        # Styling tombol khusus
        common_button_style = "font-size: 9pt; padding: 6px 8px;"
        self.paste_button.setStyleSheet(f"""
            QPushButton {{ background-color: #ffc107; border-color: #e0a800; color: #212529; {common_button_style} }}
            QPushButton:hover {{ background-color: #e0a800; border-color: #c69500; }}
            QPushButton:pressed {{ background-color: #c69500; border-color: #b08200; }}
        """)
        self.clear_button.setStyleSheet(f"""
            QPushButton {{ background-color: #6c757d; border-color: #5a6268; {common_button_style} }}
            QPushButton:hover {{ background-color: #5a6268; border-color: #545b62; }}
            QPushButton:pressed {{ background-color: #545b62; border-color: #4e555b; }}
        """)
        self.delete_button.setStyleSheet(f"""
            QPushButton {{ background-color: #dc3545; border-color: #c82333; {common_button_style} }}
            QPushButton:hover {{ background-color: #c82333; border-color: #bd2130; }}
            QPushButton:pressed {{ background-color: #bd2130; border-color: #b21e2c; }}
        """)
        self.export_button.setStyleSheet(f"""
            QPushButton {{ background-color: #28a745; border-color: #218838; {common_button_style} }}
            QPushButton:hover {{ background-color: #218838; border-color: #1e7e34; }}
            QPushButton:pressed {{ background-color: #1e7e34; border-color: #1c7430; }}
        """)
        self.name_label_top.setStyleSheet("font-size: 9pt; color: #555; font-style: italic;")
        if hasattr(self, 'status_name_label'):
            base_status_label_style = "font-size: 9pt; color: #333;"
            self.status_name_label.setStyleSheet(f"{base_status_label_style} padding-right: 8px;")
            self.status_nim_label.setStyleSheet(f"{base_status_label_style} padding-right: 3px;")
            self.status_message_label.setStyleSheet(f"{base_status_label_style} color: #111;")
            self.status_data_count_label.setStyleSheet(f"{base_status_label_style} color: #111; font-weight: bold;")


    def execute_query(self, query, params=()):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        success = False
        try:
            cursor.execute(query, params)
            conn.commit()
            # self._update_status_message("Query berhasil dieksekusi.") # Dihapus agar tidak terlalu cerewet
            success = True
        except Exception as e:
            conn.rollback()
            print(f"Database error: {e}")
            QMessageBox.critical(self, "Error Database", f"Terjadi kesalahan database: {e}")
            self._update_status_message(f"Error database: {e}")
        finally:
            conn.close()
        return cursor # Sebenarnya cursor tidak banyak berguna jika koneksi sudah ditutup, kecuali untuk lastrowid sebelum commit jika insert

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
            self._update_status_message(f"Error pengambilan data: {e}")
        finally:
            conn.close()
        return rows

    def load_data(self):
        movies = self.fetch_query("SELECT id, title, director, year, genre FROM movies ORDER BY lower(title) COLLATE NOCASE")
        self.table_widget.setRowCount(0) # Hapus semua baris sebelum memuat
        for row_number, movie in enumerate(movies):
            self.table_widget.insertRow(row_number)
            for column_number, data in enumerate(movie):
                item = QTableWidgetItem(str(data) if data is not None else "")
                if column_number == 0: item.setTextAlignment(Qt.AlignCenter)
                elif column_number == 3: item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(row_number, column_number, item)

        self._update_data_count_status(len(movies)) # Update jumlah data di status bar
        if not movies:
            self._update_status_message("Database kosong atau tidak ada data.")
        else:
            self._update_status_message(f"{len(movies)} film dimuat.")


    def save_movie(self):
        title = self.title_input.text().strip()
        director = self.director_input.text().strip()
        year_text = self.year_input.text().strip()
        genre = self.genre_input.text().strip()

        if not title:
            QMessageBox.warning(self, "Input Tidak Valid", "Judul film tidak boleh kosong.")
            self.title_input.setFocus()
            self._update_status_message("Gagal: Judul kosong.")
            return

        year = None
        if year_text: # Validasi tahun hanya jika diisi
            try:
                year_val = int(year_text)
                if not (1800 <= year_val <= 2100): # Tahun harus dalam rentang wajar
                    QMessageBox.warning(self, "Input Tidak Valid", "Tahun rilis tidak valid (antara 1800-2100).")
                    self.year_input.setFocus(); self._update_status_message("Gagal: Tahun tidak valid."); return
                year = year_val
            except ValueError:
                QMessageBox.warning(self, "Input Tidak Valid", "Tahun rilis harus berupa angka.");
                self.year_input.setFocus(); self._update_status_message("Gagal: Tahun bukan angka."); return

        # Cek duplikasi judul (lebih toleran saat update)
        query_check_duplicate = "SELECT id FROM movies WHERE lower(title) = ?"
        params_check_duplicate = (title.lower(),)
        existing_movies = self.fetch_query(query_check_duplicate, params_check_duplicate)

        is_duplicate = False
        if existing_movies:
            if self.current_movie_id is None: # Mode Tambah Baru
                is_duplicate = True
            else: # Mode Update
                if existing_movies[0][0] != self.current_movie_id: # Duplikat dengan ID lain
                    is_duplicate = True

        if is_duplicate:
            reply = QMessageBox.question(self, "Konfirmasi Judul Duplikat",
                                         f"Film dengan judul '{title}' sudah ada. Tetap simpan?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                self._update_status_message("Simpan dibatalkan (judul duplikat)."); return

        if self.current_movie_id is None:
            self.execute_query("INSERT INTO movies (title, director, year, genre) VALUES (?, ?, ?, ?)",
                               (title, director, year, genre))
            self._update_status_message(f"Film '{title}' disimpan.")
            QMessageBox.information(self, "Sukses", f"Film '{title}' berhasil disimpan.")
        else:
            self.execute_query("UPDATE movies SET title=?, director=?, year=?, genre=? WHERE id=?",
                               (title, director, year, genre, self.current_movie_id))
            self._update_status_message(f"Film '{title}' diperbarui.")
            QMessageBox.information(self, "Sukses", f"Film '{title}' berhasil diperbarui.")

        self.clear_form_action(clear_status=False) # Jangan clear status message dari save
        self.load_data()

    def clear_form_action(self, clear_status=True):
        self.current_movie_id = None
        self.title_input.clear(); self.director_input.clear()
        self.year_input.clear(); self.genre_input.clear()
        self.save_button.setText("💾 Simpan"); self.save_button.setIcon(QIcon())
        self.title_input.setFocus()
        self.table_widget.clearSelection()
        if clear_status:
            self._update_status_message("Form dibersihkan.")


    def load_movie_to_form(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows: return # Tidak ada baris terpilih

        selected_row = selected_rows[0].row() # Ambil baris pertama dari seleksi
        try:
            movie_id = int(self.table_widget.item(selected_row, 0).text())
            title = self.table_widget.item(selected_row, 1).text()
            director = self.table_widget.item(selected_row, 2).text() if self.table_widget.item(selected_row, 2) else ""
            year = self.table_widget.item(selected_row, 3).text() if self.table_widget.item(selected_row, 3) else ""
            genre = self.table_widget.item(selected_row, 4).text() if self.table_widget.item(selected_row, 4) else ""

            self.current_movie_id = movie_id
            self.title_input.setText(title)
            self.director_input.setText(director)
            self.year_input.setText(year if year != "None" else "")
            self.genre_input.setText(genre if genre != "None" else "")
            self.save_button.setText("💾 Perbarui") # Tombol update
            self._update_status_message(f"Film '{title}' dimuat ke form.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data film ke form: {e}")
            self._update_status_message(f"Error memuat: {e}")
            self.clear_form_action()


    def delete_movie_action(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Tidak Ada Pilihan", "Pilih film yang ingin dihapus.");
            self._update_status_message("Hapus gagal: Tidak ada pilihan."); return

        movie_id = self.table_widget.item(selected_rows[0].row(), 0).text()
        movie_title = self.table_widget.item(selected_rows[0].row(), 1).text()

        reply = QMessageBox.question(self, "Konfirmasi Hapus",
                                     f"Yakin ingin menghapus '{movie_title}' (ID: {movie_id})?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.execute_query("DELETE FROM movies WHERE id=?", (movie_id,))
            self._update_status_message(f"Film '{movie_title}' dihapus.")
            QMessageBox.information(self, "Sukses", f"Film '{movie_title}' berhasil dihapus.")
            if self.current_movie_id == int(movie_id): # Jika yang diedit dihapus
                self.clear_form_action(clear_status=False)
            self.load_data()
        else:
            self._update_status_message("Hapus dibatalkan.")

    def search_movies(self):
        search_text = self.search_input.text().lower().strip()
        visible_rows = 0
        for i in range(self.table_widget.rowCount()):
            title_item = self.table_widget.item(i, 1)
            director_item = self.table_widget.item(i, 2)
            genre_item = self.table_widget.item(i, 4)

            match = False
            if search_text: # Hanya filter jika ada teks pencarian
                title_match = title_item and search_text in title_item.text().lower()
                director_match = director_item and search_text in director_item.text().lower()
                genre_match = genre_item and search_text in genre_item.text().lower()
                match = title_match or director_match or genre_match
            else: # Jika search_text kosong, tampilkan semua
                match = True

            self.table_widget.setRowHidden(i, not match)
            if match:
                visible_rows +=1

        if search_text:
            self._update_status_message(f"Filter '{search_text}': {visible_rows} hasil.")
        else: # Jika search dikosongkan, tampilkan jumlah total dari status data count
            current_total = self.status_data_count_label.text().split(':')[-1].strip()
            self._update_status_message(f"Menampilkan semua {current_total} data.")


    def export_to_csv_action(self):
        if self.table_widget.rowCount() == 0:
            QMessageBox.information(self, "Data Kosong", "Tidak ada data untuk diekspor.");
            self._update_status_message("Ekspor gagal: Data kosong."); return

        # Mengambil nama dan nim dari status bar untuk nama file default
        nim_for_file = self.status_nim_label.text().replace("NIM: ", "").strip()
        nama_for_file = self.status_name_label.text().replace(" ", "_").strip()
        default_filename = f"koleksi_film_{nama_for_file}_{nim_for_file}.csv"

        path, _ = QFileDialog.getSaveFileName(self, "Ekspor Data ke CSV", default_filename,
                                              "CSV Files (*.csv);;All Files (*)")
        if path:
            try:
                with open(path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]
                    writer.writerow(headers)
                    for row in range(self.table_widget.rowCount()):
                        if not self.table_widget.isRowHidden(row):
                            writer.writerow([self.table_widget.item(row, col).text() if self.table_widget.item(row, col) else ''
                                             for col in range(self.table_widget.columnCount())])
                QMessageBox.information(self, "Ekspor Berhasil", f"Data diekspor ke:\n{path}")
                self._update_status_message(f"Data diekspor ke {path.split('/')[-1]}.")
            except Exception as e:
                QMessageBox.critical(self, "Error Ekspor", f"Gagal mengekspor data: {e}");
                self._update_status_message(f"Error ekspor: {e}.")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Konfirmasi Keluar', "Yakin ingin keluar?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._update_status_message("Aplikasi ditutup."); event.accept()
        else:
            self._update_status_message("Keluar dibatalkan."); event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyle('Fusion')
    window = MovieApp()
    window.show()
    sys.exit(app.exec_())
