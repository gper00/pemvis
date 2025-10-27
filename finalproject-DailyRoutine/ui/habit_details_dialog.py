"""
A custom dialog to show detailed information about a habit in a clean, professional layout.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QPushButton, QHBoxLayout,
    QFrame, QTextBrowser, QDialogButtonBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from utils.helpers import format_date_for_display, get_priority_color, get_status_color

class HabitDetailsDialog(QDialog):
    """A dialog to display habit details."""
    # Signal: habit_id, new_status
    status_change_requested = pyqtSignal(int, str)

    def __init__(self, habit_data, parent=None):
        super().__init__(parent)
        self.habit_data = habit_data

        self.setWindowTitle("Habit Details")
        self.setMinimumWidth(450)
        self.setObjectName("detailsDialog")

        self.setup_ui()
        self.load_data()
        self.setup_styling()

    def setup_ui(self):
        """Setup the user interface."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title
        self.name_label = QLabel()
        self.name_label.setObjectName("detailsTitle")
        self.name_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.name_label.setWordWrap(True)
        main_layout.addWidget(self.name_label)

        # Main details using QFormLayout
        details_frame = QFrame()
        details_frame.setObjectName("detailsFrame")
        form_layout = QFormLayout(details_frame)
        form_layout.setContentsMargins(15, 15, 15, 15)
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.category_label = QLabel()
        self.frequency_label = QLabel()
        self.start_date_label = QLabel()
        self.status_label = QLabel()
        self.priority_label = QLabel()
        self.target_label = QLabel()
        self.progress_label = QLabel()

        form_layout.addRow(QLabel("<strong>Category:</strong>"), self.category_label)
        form_layout.addRow(QLabel("<strong>Frequency:</strong>"), self.frequency_label)
        form_layout.addRow(QLabel("<strong>Start Date:</strong>"), self.start_date_label)
        form_layout.addRow(QLabel("<strong>Status:</strong>"), self.status_label)
        form_layout.addRow(QLabel("<strong>Priority:</strong>"), self.priority_label)
        form_layout.addRow(QLabel("<strong>Weekly Target:</strong>"), self.target_label)
        form_layout.addRow(QLabel("<strong>Progress:</strong>"), self.progress_label)

        main_layout.addWidget(details_frame)

        # Notes section
        notes_frame = QFrame()
        notes_frame.setObjectName("notesFrame")
        notes_layout = QVBoxLayout(notes_frame)
        notes_layout.setContentsMargins(15, 15, 15, 15)
        notes_layout.setSpacing(8)

        notes_title = QLabel("Notes")
        notes_title.setObjectName("notesTitle")
        notes_title.setFont(QFont("Segoe UI", 12, QFont.Bold))

        self.notes_content = QLabel()
        self.notes_content.setWordWrap(True)
        self.notes_content.setAlignment(Qt.AlignTop)

        notes_layout.addWidget(notes_title)
        notes_layout.addWidget(self.notes_content)
        main_layout.addWidget(notes_frame)

        # Timestamps
        timestamp_layout = QHBoxLayout()
        self.created_label = QLabel()
        self.updated_label = QLabel()
        timestamp_layout.addWidget(self.created_label)
        timestamp_layout.addStretch()
        timestamp_layout.addWidget(self.updated_label)
        main_layout.addLayout(timestamp_layout)

        # Action Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.status_button = QPushButton()
        self.status_button.setObjectName("statusButton")
        self.status_button.clicked.connect(self.request_status_change)

        button_layout.addStretch()
        button_layout.addWidget(self.status_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        main_layout.addLayout(button_layout)

    def load_data(self):
        """Load habit data into the widgets."""
        self.name_label.setText(self.habit_data.get('name', 'N/A'))
        self.category_label.setText(self.habit_data.get('category', 'N/A'))
        self.frequency_label.setText(f"{self.habit_data.get('frequency', 0)} times per week")
        self.start_date_label.setText(format_date_for_display(self.habit_data.get('start_date', '')))

        status = self.habit_data.get('status', 'N/A')
        status_color = get_status_color(status)
        self.status_label.setText(f'<strong style="color: {status_color};">{status}</strong>')

        # Update status button
        if status == 'Selesai':
            self.status_button.setText("Mark as Incomplete")
            self.status_button.setProperty("isComplete", False)
        else:
            self.status_button.setText("Mark as Complete")
            self.status_button.setProperty("isComplete", True)
        self.status_button.style().polish(self.status_button)

        priority = self.habit_data.get('priority', 'N/A')
        priority_color = get_priority_color(priority)
        self.priority_label.setText(f'<strong style="color: {priority_color};">{priority}</strong>')

        self.target_label.setText(f"{self.habit_data.get('target_weekly', 1)} times")
        self.progress_label.setText(
            f"Streak: {self.habit_data.get('streak_count', 0)} days | "
            f"Total Completed: {self.habit_data.get('total_completed', 0)} times"
        )
        self.notes_content.setText(self.habit_data.get('notes') or "No notes available.")

        self.created_label.setText(f"Created: {format_date_for_display(self.habit_data.get('created_at', ''))}")
        self.updated_label.setText(f"Last Updated: {format_date_for_display(self.habit_data.get('updated_at', ''))}")

    def request_status_change(self):
        """Emit a signal to request a status change and then close."""
        current_status = self.habit_data.get('status', 'Belum')
        new_status = 'Selesai' if current_status == 'Belum' else 'Belum'
        self.status_change_requested.emit(self.habit_data['id'], new_status)
        self.accept() # Close the dialog

    def setup_styling(self):
        """Set the stylesheet for the dialog."""
        self.setStyleSheet("""
            #detailsDialog {
                background-color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            #detailsTitle {
                color: #212529;
            }
            #detailsFrame, #notesFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }
            QLabel {
                color: #495057;
                font-size: 13px;
            }
            #notesTitle {
                color: #212529;
            }
            QPushButton {
                background-color: #f8f9fa;
                color: #495057;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                font-weight: 500;
                padding: 10px 20px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
            #statusButton[isComplete="true"] {
                background-color: #28a745;
                border-color: #28a745;
                color: white;
            }
            #statusButton[isComplete="true"]:hover {
                background-color: #218838;
            }
            #statusButton[isComplete="false"] {
                background-color: #ffc107;
                border-color: #ffc107;
                color: #212529;
            }
            #statusButton[isComplete="false"]:hover {
                background-color: #e0a800;
            }
        """)
