import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QFormLayout, QComboBox, QPushButton, QMessageBox, QTextEdit, QFrame)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QFont

class FormValidationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Task Week 5 - Validation')
        self.setGeometry(300, 300, 500, 500)
        self.setStyleSheet("background-color: #f0f0f0;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        identity_frame = QFrame()
        identity_layout = QVBoxLayout()
        identity_layout.setContentsMargins(10, 10, 10, 10)

        name_label = QLabel('Nama: UMAM ALPARIZI')
        name_label.setFont(QFont('Arial', 10))
        name_label.setAlignment(Qt.AlignCenter)

        nim_label = QLabel('NIM: F1D02310141')
        nim_label.setFont(QFont('Arial', 10))
        nim_label.setAlignment(Qt.AlignCenter)

        identity_layout.addWidget(name_label)
        identity_layout.addWidget(nim_label)
        identity_frame.setLayout(identity_layout)

        main_layout.addWidget(identity_frame)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #d0d0d0;")
        main_layout.addWidget(line)

        form_container = QWidget()
        form_container_layout = QVBoxLayout()
        form_container_layout.setContentsMargins(10, 20, 10, 10)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignRight)

        input_style = """
            QLineEdit, QTextEdit, QComboBox {
                border: 1px solid #aaa;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 1px solid #3498db;
            }
        """

        # Name input
        self.name_input = QLineEdit()
        # self.name_input.setPlaceholderText('Enter your name (4-100 characters)')
        self.name_input.setStyleSheet(input_style)
        form_layout.addRow('Name:', self.name_input)

        # Email input
        self.email_input = QLineEdit()
        # self.email_input.setPlaceholderText('example@domain.com')
        self.email_input.setStyleSheet(input_style)
        form_layout.addRow('Email:', self.email_input)

        # Age input
        self.age_input = QLineEdit()
        # self.age_input.setPlaceholderText('Must be a number that greater than 1')
        self.age_input.setStyleSheet(input_style)
        # Only allow numbers
        age_validator = QRegExpValidator(QRegExp(r'[0-9]+'))
        self.age_input.setValidator(age_validator)
        form_layout.addRow('Age:', self.age_input)

        # Phone number input with mask
        self.phone_input = QLineEdit()
        # self.phone_input.setPlaceholderText('+62 xxx xxxx xxxx')
        self.phone_input.setInputMask('+62 999 9999 9999')
        self.phone_input.setStyleSheet(input_style)
        form_layout.addRow('Phone Number:', self.phone_input)

        # Address input
        self.address_input = QTextEdit()
        # self.address_input.setPlaceholderText('Enter your address')
        self.address_input.setStyleSheet(input_style)
        self.address_input.setMaximumHeight(100)
        form_layout.addRow('Address:', self.address_input)

        # Gender dropdown
        self.gender_combo = QComboBox()
        self.gender_combo.addItem('Select Gender')
        self.gender_combo.addItem('Male')
        self.gender_combo.addItem('Female')
        self.gender_combo.setStyleSheet(input_style)
        form_layout.addRow('Gender:', self.gender_combo)

        # Education dropdown
        self.education_combo = QComboBox()
        self.education_combo.addItem('Select Education')
        self.education_combo.addItem('High School')
        self.education_combo.addItem('Bachelor')
        self.education_combo.addItem('Master')
        self.education_combo.addItem('PhD')
        self.education_combo.setStyleSheet(input_style)
        form_layout.addRow('Education:', self.education_combo)

        form_container_layout.addLayout(form_layout)

        button_container = QHBoxLayout()
        button_container.setContentsMargins(0, 20, 0, 0)

        label_spacer = QWidget()
        button_container.addWidget(label_spacer)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.save_button = QPushButton('Save')
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.clicked.connect(self.validate_and_save)

        self.clear_button = QPushButton('Clear')
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.clicked.connect(self.clear_form)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()  # Add stretch to push buttons to the left

        button_container.addLayout(button_layout)

        button_container.setStretch(0, form_layout.labelAlignment())  # Label width
        button_container.setStretch(1, 1)  # Field width

        form_container_layout.addLayout(button_container)
        form_container.setLayout(form_container_layout)

        main_layout.addWidget(form_container)

        self.setLayout(main_layout)

        # Set keyboard shortcut to close app (Q)
        self.shortcut = Qt.Key_Q

        self.show()
        self.adjust_button_alignment()

    def adjust_button_alignment(self):
        """Adjust button alignment to match the input fields after the form is rendered"""
        form_layout = self.findChild(QFormLayout)
        if form_layout:
            label_width = 0
            for i in range(form_layout.rowCount()):
                label_item = form_layout.itemAt(i, QFormLayout.LabelRole)
                if label_item and label_item.widget():
                    label_width = max(label_width, label_item.widget().sizeHint().width())

            for button in [self.save_button, self.clear_button]:
                button.setContentsMargins(label_width + 10, 0, 0, 0)

    def keyPressEvent(self, event):
        if event.key() == self.shortcut:
            self.close()
        else:
            super().keyPressEvent(event)

    def validate_and_save(self):
        errors = []

        # Validate Name
        name = self.name_input.text().strip()
        if not name:
            errors.append("Name is required")
        elif len(name) < 4 or len(name) > 100:
            errors.append("Name must be between 4 and 100 characters")

        # Validate Email
        email = self.email_input.text().strip()
        email_regex = QRegExp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email:
            errors.append("Email is required")
        elif not email_regex.exactMatch(email):
            errors.append("Email format is invalid")

        # Validate Age
        age = self.age_input.text().strip()
        if not age:
            errors.append("Age is required")
        elif int(age) <= 1:
            errors.append("Age must be greater than 1")

        # Validate Phone Number
        phone = self.phone_input.text().strip()
        # Remove non-digit characters for validation
        digits_only = ''.join(filter(str.isdigit, phone))
        if len(digits_only) != 13:
            errors.append("Phone number must be 13 digits")

        # Validate Address
        address = self.address_input.toPlainText().strip()
        if not address:
            errors.append("Address is required")

        # Validate Gender
        if self.gender_combo.currentIndex() == 0:
            errors.append("Please select a gender")

        # Validate Education
        if self.education_combo.currentIndex() == 0:
            errors.append("Please select education level")

        # Display errors if any
        if errors:
            error_message = "\n".join(errors)
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Warning)
            error_box.setWindowTitle("Validation Error")
            error_box.setText("Please fix the following errors:")
            error_box.setDetailedText(error_message)
            error_box.exec_()
        else:
            success_box = QMessageBox()
            success_box.setIcon(QMessageBox.Information)
            success_box.setWindowTitle("Success")
            success_box.setText("Form submitted successfully!")
            success_box.exec_()
            self.clear_form()

    def clear_form(self):
        self.name_input.clear()
        self.email_input.clear()
        self.age_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.gender_combo.setCurrentIndex(0)
        self.education_combo.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = FormValidationApp()
    window.show()
    sys.exit(app.exec_())


# Tambahan kriteria validasi:
# - Nama: harus masuk dalam rentang 4 - 100 karakter
# - Usia: harus lebih dari 0
