import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout, QRadioButton,
    QComboBox, QGroupBox, QFrame
)

class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tugas Week 2 : Layout and Styling")
        self.setGeometry(100, 100, 500, 450)
        self.setStyleSheet("background-color: #ECECEC;")

        # Identitas (Vertical Layout)
        identitas_box = QGroupBox("Identitas")
        identitas_layout = QVBoxLayout()
        identitas_layout.addWidget(QLabel("Nama : UMAM ALPARIZI"))
        identitas_layout.addWidget(QLabel("Nim : F1D02310141"))
        identitas_layout.addWidget(QLabel("Kelas: Pemrograman Visual 6C"))
        identitas_box.setLayout(identitas_layout)

        # Navigasi (Horizontal Layout)
        nav_box = QGroupBox("Navigation")
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(QPushButton("Home"))
        nav_layout.addWidget(QPushButton("About"))
        nav_layout.addWidget(QPushButton("Contact"))
        nav_box.setLayout(nav_layout)

        # Form Registrasi (Form Layout)
        form_box = QGroupBox("User Registration")
        form_layout = QFormLayout()

        self.fullname = QLineEdit()
        self.email = QLineEdit()
        self.phone = QLineEdit()

        form_layout.addRow("Full Name:", self.fullname)
        form_layout.addRow("Email:", self.email)
        form_layout.addRow("Phone:", self.phone)

        # Gender (Horizontal Layout)
        gender_layout = QHBoxLayout()
        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        form_layout.addRow("Gender:", gender_layout)

        # Country (Dropdown)
        self.country_combo = QComboBox()
        self.country_combo.addItems(["", "Indonesia", "USA", "UK", "Japan"])
        form_layout.addRow("Country:", self.country_combo)

        form_box.setLayout(form_layout)

        # Actions (Horizontal Layout)
        action_box = QGroupBox("Actions")
        action_layout = QHBoxLayout()
        action_layout.addWidget(QPushButton("Submit"))
        action_layout.addWidget(QPushButton("Cancel"))
        action_box.setLayout(action_layout)

        # Border Line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        # Layout Utama (Vertical)
        main_layout = QVBoxLayout()
        main_layout.addWidget(identitas_box)
        main_layout.addWidget(nav_box)
        main_layout.addWidget(form_box)
        main_layout.addWidget(action_box)

        self.setLayout(main_layout)

        # Gaya Kustom (CSS)
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                background-color: #F8F8F8;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton {
                padding: 5px;
                background-color: #D3D3D3;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #C0C0C0;
            }
            QLineEdit, QComboBox {
                background-color: white;
                padding: 3px;
                border-radius: 3px;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationForm()
    window.show()
    sys.exit(app.exec_())
