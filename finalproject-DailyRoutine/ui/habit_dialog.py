"""
Habit Dialog for adding and editing habits
"""

import sys
from datetime import date
from typing import Dict, Any, Optional
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QComboBox, QSpinBox, QDateEdit, QTextEdit, QPushButton, QMessageBox,
    QGroupBox, QFrame
)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from config.constants import (
    HABIT_CATEGORIES, HABIT_PRIORITIES, HABIT_STATUS,
    MIN_FREQUENCY, MAX_FREQUENCY, MAX_HABIT_NAME_LENGTH, MAX_NOTES_LENGTH
)

class HabitDialog(QDialog):
    """Dialog for adding and editing habits"""

    habit_saved = pyqtSignal(dict)  # Signal emitted when habit is saved

    def __init__(self, parent=None, habit_data: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        self.habit_data = habit_data
        self.is_editing = habit_data is not None

        self.setup_ui()
        self.setup_styling()
        self.setup_connections()

        if self.is_editing:
            self.load_habit_data()
            self.setWindowTitle("Edit Habit")
        else:
            self.setWindowTitle("Add New Habit")

    def setup_ui(self):
        """Setup the user interface"""
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)

        # Main layout
        main_layout = QVBoxLayout()

        # Form group
        form_group = QGroupBox("Habit Information")
        form_layout = QFormLayout()

        # Name field
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter habit name...")
        self.name_edit.setMaxLength(MAX_HABIT_NAME_LENGTH)
        form_layout.addRow("Nama Kebiasaan *:", self.name_edit)

        # Category field
        self.category_combo = QComboBox()
        self.category_combo.addItems(HABIT_CATEGORIES)
        form_layout.addRow("Kategori *:", self.category_combo)

        # Frequency field
        self.frequency_spin = QSpinBox()
        self.frequency_spin.setRange(MIN_FREQUENCY, MAX_FREQUENCY)
        self.frequency_spin.setValue(1)
        self.frequency_spin.setSuffix(" times per week")
        form_layout.addRow("Frekuensi *:", self.frequency_spin)

        # Start date field
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate())
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat("dd/MM/yyyy")
        form_layout.addRow("Tanggal Mulai *:", self.start_date_edit)

        # Status field
        self.status_combo = QComboBox()
        self.status_combo.addItems(HABIT_STATUS)
        form_layout.addRow("Status:", self.status_combo)

        # Priority field
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(HABIT_PRIORITIES)
        self.priority_combo.setCurrentText("Medium")
        form_layout.addRow("Prioritas:", self.priority_combo)

        # Target weekly field
        self.target_weekly_spin = QSpinBox()
        self.target_weekly_spin.setRange(1, 7)
        self.target_weekly_spin.setValue(1)
        self.target_weekly_spin.setSuffix(" times")
        form_layout.addRow("Target Mingguan:", self.target_weekly_spin)

        # Notes field
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Enter additional notes...")
        self.notes_edit.setMaximumHeight(100)
        form_layout.addRow("Catatan:", self.notes_edit)

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        # Character count labels
        char_layout = QHBoxLayout()
        self.name_char_count = QLabel(f"0/{MAX_HABIT_NAME_LENGTH}")
        self.name_char_count.setStyleSheet("color: gray; font-size: 10px;")
        char_layout.addWidget(self.name_char_count)
        char_layout.addStretch()

        self.notes_char_count = QLabel(f"0/{MAX_NOTES_LENGTH}")
        self.notes_char_count.setStyleSheet("color: gray; font-size: 10px;")
        char_layout.addWidget(self.notes_char_count)
        main_layout.addLayout(char_layout)

        # Buttons
        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Save")
        self.save_button.setDefault(True)
        self.save_button.setMinimumWidth(100)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumWidth(100)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setMinimumWidth(100)

        button_layout.addStretch()
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def setup_styling(self):
        """Setup dialog styling"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }

            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }

            QLineEdit, QComboBox, QSpinBox, QDateEdit, QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 8px 10px;
                background-color: #ffffff;
                font-size: 13px;
                color: #495057;
            }

            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus, QTextEdit:focus {
                border-color: #80bdff;
            }

            QComboBox::drop-down, QDateEdit::drop-down-button {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: #ced4da;
                border-left-style: solid;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }

            QComboBox::down-arrow, QDateEdit::down-arrow {
                image: url(assets/icons/chevron-down.svg);
                width: 16px;
                height: 16px;
            }

            QSpinBox::up-button, QSpinBox::down-button {
                subcontrol-origin: border;
                width: 20px;
                background-color: #f8f9fa;
                border: 1px solid #ced4da;
            }

            QSpinBox::up-button {
                subcontrol-position: top right;
                border-top-right-radius: 6px;
            }

            QSpinBox::down-button {
                subcontrol-position: bottom right;
                border-bottom-right-radius: 6px;
            }

            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #e9ecef;
            }

            QSpinBox::up-arrow {
                image: url(assets/icons/chevron-up.svg);
                width: 12px;
                height: 12px;
            }

            QSpinBox::down-arrow {
                image: url(assets/icons/chevron-down.svg);
                width: 12px;
                height: 12px;
            }

            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }

            QPushButton:hover {
                background-color: #0069d9;
            }

            QPushButton:pressed {
                background-color: #0056b3;
            }

            #cancelButton {
                background-color: #6c757d;
            }

            #cancelButton:hover {
                background-color: #5a6268;
            }

            #resetButton {
                background-color: #ffc107;
                color: #212529;
            }

            #resetButton:hover {
                background-color: #e0a800;
            }
        """)

        # Set button object names for specific styling
        self.cancel_button.setObjectName("cancelButton")
        self.reset_button.setObjectName("resetButton")

    def setup_connections(self):
        """Setup signal connections"""
        self.save_button.clicked.connect(self.save_habit)
        self.cancel_button.clicked.connect(self.reject)
        self.reset_button.clicked.connect(self.reset_form)

        # Character count updates
        self.name_edit.textChanged.connect(self.update_name_char_count)
        self.notes_edit.textChanged.connect(self.update_notes_char_count)

    def update_name_char_count(self):
        """Update name character count"""
        count = len(self.name_edit.text())
        self.name_char_count.setText(f"{count}/{MAX_HABIT_NAME_LENGTH}")

        # Change color based on length
        if count > MAX_HABIT_NAME_LENGTH * 0.9:
            self.name_char_count.setStyleSheet("color: red; font-size: 10px;")
        elif count > MAX_HABIT_NAME_LENGTH * 0.7:
            self.name_char_count.setStyleSheet("color: orange; font-size: 10px;")
        else:
            self.name_char_count.setStyleSheet("color: gray; font-size: 10px;")

    def update_notes_char_count(self):
        """Update notes character count"""
        count = len(self.notes_edit.toPlainText())
        self.notes_char_count.setText(f"{count}/{MAX_NOTES_LENGTH}")

        # Change color based on length
        if count > MAX_NOTES_LENGTH * 0.9:
            self.notes_char_count.setStyleSheet("color: red; font-size: 10px;")
        elif count > MAX_NOTES_LENGTH * 0.7:
            self.notes_char_count.setStyleSheet("color: orange; font-size: 10px;")
        else:
            self.notes_char_count.setStyleSheet("color: gray; font-size: 10px;")

    def load_habit_data(self):
        """Load existing habit data into form"""
        if not self.habit_data:
            return

        try:
            self.name_edit.setText(self.habit_data.get('name', ''))
            self.category_combo.setCurrentText(self.habit_data.get('category', 'Umum'))
            self.frequency_spin.setValue(self.habit_data.get('frequency', 1))

            # Load start date
            start_date_str = self.habit_data.get('start_date', '')
            if start_date_str:
                try:
                    start_date = QDate.fromString(start_date_str[:10], "yyyy-MM-dd")
                    self.start_date_edit.setDate(start_date)
                except:
                    self.start_date_edit.setDate(QDate.currentDate())

            self.status_combo.setCurrentText(self.habit_data.get('status', 'Belum'))
            self.priority_combo.setCurrentText(self.habit_data.get('priority', 'Medium'))
            self.target_weekly_spin.setValue(self.habit_data.get('target_weekly', 1))
            self.notes_edit.setPlainText(self.habit_data.get('notes', ''))

            # Update character counts
            self.update_name_char_count()
            self.update_notes_char_count()

        except Exception as e:
            print(f"Error loading habit data: {e}")
            QMessageBox.warning(self, "Error", f"Error loading habit data: {e}")

    def get_form_data(self) -> Dict[str, Any]:
        """Get data from form fields"""
        return {
            'name': self.name_edit.text().strip(),
            'category': self.category_combo.currentText(),
            'frequency': self.frequency_spin.value(),
            'start_date': self.start_date_edit.date().toString("yyyy-MM-dd"),
            'status': self.status_combo.currentText(),
            'priority': self.priority_combo.currentText(),
            'target_weekly': self.target_weekly_spin.value(),
            'notes': self.notes_edit.toPlainText().strip()
        }

    def validate_form(self) -> bool:
        """Validate form data"""
        try:
            form_data = self.get_form_data()
            errors = HabitValidator.validate_habit_data(form_data)

            if errors:
                error_message = "Please fix the following errors:\n\n" + "\n".join(f"• {error}" for error in errors)
                QMessageBox.warning(self, "Validation Error", error_message)
                return False

            return True

        except Exception as e:
            print(f"Error validating form: {e}")
            QMessageBox.critical(self, "Error", f"Error validating form: {e}")
            return False

    def save_habit(self):
        """Validate and save habit data."""
        habit_name = self.name_edit.text().strip()
        if not habit_name:
            QMessageBox.warning(self, "Input Error", "Nama Kebiasaan tidak boleh kosong.")
            self.name_edit.setFocus()
            return

        try:
            data = self.get_form_data()
            if self.is_editing:
                data['id'] = self.habit_data['id']

            self.habit_saved.emit(data)
            self.accept()
        except Exception as e:
            print(f"Error saving habit form: {e}")
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat menyimpan: {e}")

    def reset_form(self):
        """Reset form to default values"""
        if self.is_editing:
            self.load_habit_data()
        else:
            self.name_edit.clear()
            self.category_combo.setCurrentIndex(0)
            self.frequency_spin.setValue(1)
            self.start_date_edit.setDate(QDate.currentDate())
            self.status_combo.setCurrentIndex(0)
            self.priority_combo.setCurrentText("Medium")
            self.target_weekly_spin.setValue(1)
            self.notes_edit.clear()

        # Reset validations styles if any
        self.validate_name()
        self.validate_category()
        self.validate_frequency()

    def closeEvent(self, event):
        """Handle dialog close event."""
        if self.has_unsaved_changes():
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Are you sure you want to exit?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                self.save_habit()
            elif reply == QMessageBox.Cancel:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()

    def has_unsaved_changes(self) -> bool:
        """Check if form has been modified."""
        if not self.is_editing and (self.name_edit.text() or self.notes_edit.toPlainText()):
            return True

        if self.is_editing:
            original_data = {
                "name": self.habit_data.get('name', ''),
                "category": self.habit_data.get('category', 'Umum'),
                "frequency": self.habit_data.get('frequency', 1),
                "start_date": QDate.fromString(self.habit_data.get('start_date', ''), "yyyy-MM-dd"),
                "status": self.habit_data.get('status', 'Belum'),
                "priority": self.habit_data.get('priority', 'Medium'),
                "target_weekly": self.habit_data.get('target_weekly', 1),
                "notes": self.habit_data.get('notes', ''),
            }

            current_data = {
                "name": self.name_edit.text(),
                "category": self.category_combo.currentText(),
                "frequency": self.frequency_spin.value(),
                "start_date": self.start_date_edit.date(),
                "status": self.status_combo.currentText(),
                "priority": self.priority_combo.currentText(),
                "target_weekly": self.target_weekly_spin.value(),
                "notes": self.notes_edit.toPlainText(),
            }

            return original_data != current_data

        return False
