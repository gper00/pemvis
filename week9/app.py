import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QInputDialog, QLineEdit, QPushButton, QComboBox,
                            QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

class LanguageDialog(QDialog):
    def __init__(self, parent=None, selected_language=None):
        super().__init__(parent)
        self.setWindowTitle("Pilih Bahasa Pemrograman")
        self.resize(300, 150)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #333;
            }
            QComboBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 3px;
                min-height: 20px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: #ccc;
                border-left-style: solid;
            }
            QPushButton {
                background-color: #4285f4;
                color: white;
                padding: 4px 8px;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3367d6;
            }
            QPushButton:pressed {
                background-color: #2a56c6;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Title label
        title_label = QLabel("Pilih Bahasa Pemrograman:")
        title_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(title_label)

        # Programming languages combobox (select option)
        self.lang_combo = QComboBox()

        # Add language options
        languages = ["C", "C++", "Python", "Java", "JavaScript"]
        self.lang_combo.addItems(languages)

        # Set initial selection if provided
        if selected_language and selected_language in languages:
            self.lang_combo.setCurrentText(selected_language)

        main_layout.addWidget(self.lang_combo)

        # Standard button box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.setStyleSheet("""
            QPushButton {
                min-width: 60px;
            }
        """)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

    def get_selected_language(self):
        return self.lang_combo.currentText()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_language = ""
        self.name = ""
        self.entry_year = 2023
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Week 9: Qtab 7 Input Dialog')
        self.resize(450, 200)

        # Set the application style
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton {
                background-color: #4285f4;
                color: white;
                padding: 5px 10px;
                border: none;
                border-radius: 3px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #3367d6;
            }
            QPushButton:pressed {
                background-color: #2a56c6;
            }
            QLabel {
                font-size: 13px;
                color: #333;
                padding: 3px 5px;
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 3px;
                min-width: 200px;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title_label = QLabel("Form Input Application")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #4285f4;
            background-color: transparent;
            border: none;
            padding: 5px;
        """)
        main_layout.addWidget(title_label)

        # Languages display
        lang_layout = QHBoxLayout()
        lang_button = QPushButton("Bahasa Pemrograman")
        lang_button.clicked.connect(self.show_language_dialog)
        self.lang_display = QLabel("Belum dipilih")
        self.lang_display.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        lang_layout.addWidget(lang_button)
        lang_layout.addWidget(self.lang_display)
        main_layout.addLayout(lang_layout)

        # Name display
        name_layout = QHBoxLayout()
        name_button = QPushButton("Nama")
        name_button.clicked.connect(self.show_name_dialog)
        self.name_display = QLabel("Belum diisi")
        self.name_display.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        name_layout.addWidget(name_button)
        name_layout.addWidget(self.name_display)
        main_layout.addLayout(name_layout)

        # Year display
        year_layout = QHBoxLayout()
        year_button = QPushButton("Tahun Masuk")
        year_button.clicked.connect(self.show_year_dialog)
        self.year_display = QLabel("2023")
        self.year_display.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        year_layout.addWidget(year_button)
        year_layout.addWidget(self.year_display)
        main_layout.addLayout(year_layout)

        self.setLayout(main_layout)

    def show_language_dialog(self):
        dialog = LanguageDialog(self, self.selected_language)
        if dialog.exec_():
            self.selected_language = dialog.get_selected_language()
            if self.selected_language:
                self.lang_display.setText(self.selected_language)
            else:
                self.lang_display.setText("Belum dipilih")

    def show_name_dialog(self):
        name, ok = QInputDialog.getText(self, "Input Nama", "Masukkan nama:",
                                        QLineEdit.Normal, self.name)
        if ok and name:
            self.name = name
            self.name_display.setText(name)

    def show_year_dialog(self):
        year, ok = QInputDialog.getInt(self, "Input Tahun Masuk", "Masukkan tahun masuk:",
                                      self.entry_year, 1970, 2025, 1)
        if ok:
            self.entry_year = year
            self.year_display.setText(str(year))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
