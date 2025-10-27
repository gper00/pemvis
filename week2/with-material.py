import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout, QRadioButton, QComboBox, QGroupBox
)
from qt_material import apply_stylesheet

class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tugas Week 2 : Layout and Styling")
        self.setGeometry(100, 100, 450, 400)

        # Identitas (Vertical Layout)
        identitas_box = QGroupBox("Identitas")
        identitas_layout = QVBoxLayout()
        identitas_layout.addWidget(QLabel("Nama \t: UMAM ALPARIZI"))
        identitas_layout.addWidget(QLabel("Nim \t: F1D02310141"))
        identitas_layout.addWidget(QLabel("Kelas \t: Pemrograman Visual 6C"))
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

        # Layout Utama (Vertical)
        main_layout = QVBoxLayout()
        main_layout.addWidget(identitas_box)
        main_layout.addWidget(nav_box)
        main_layout.addWidget(form_box)
        main_layout.addWidget(action_box)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationForm()

    apply_stylesheet(app, theme='light_blue.xml')

    window.show()
    sys.exit(app.exec_())
