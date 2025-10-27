"""
Habit List Item Widget
"""

from typing import Dict, Any
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from utils.helpers import get_priority_color, get_status_color, format_date_for_display

class HabitListItem(QFrame):
    """A compact widget for displaying a habit in a list view."""

    edit_clicked = pyqtSignal(int)
    delete_clicked = pyqtSignal(int)
    status_changed = pyqtSignal(int, str)
    details_clicked = pyqtSignal(int)

    def __init__(self, habit_data: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.habit_data = habit_data
        self.habit_id = habit_data.get('id')
        self.setup_ui()
        self.update_display()
        self.setup_connections()

    def setup_ui(self):
        """Setup the user interface."""
        self.setObjectName("habitListItem")
        self.setFrameShape(QFrame.StyledPanel)
        self.setMinimumHeight(65)
        self.setMaximumHeight(65)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 8, 15, 8)
        main_layout.setSpacing(15)

        # Priority Indicator
        self.priority_indicator = QFrame()
        self.priority_indicator.setFixedWidth(5)
        main_layout.addWidget(self.priority_indicator)

        # Name and Category
        info_layout = QVBoxLayout()
        info_layout.setSpacing(0)
        self.name_label = QLabel("Habit Name")
        self.name_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.name_label.setStyleSheet("color: #343a40;")

        self.category_label = QLabel("Category")
        self.category_label.setFont(QFont("Segoe UI", 9))
        self.category_label.setStyleSheet("color: #6c757d;")

        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.category_label)
        info_layout.addStretch()
        main_layout.addLayout(info_layout, 1) # Add stretch factor

        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Date
        self.date_label = QLabel("DD/MM/YYYY")
        self.date_label.setFont(QFont("Segoe UI", 9))
        self.date_label.setStyleSheet("color: #6c757d;")
        self.date_label.setMinimumWidth(80)
        main_layout.addWidget(self.date_label)

        # Status Badge
        self.status_label = QLabel("Status")
        self.status_label.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.status_label.setMinimumWidth(80)
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Action Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        self.details_button = QPushButton("Details")
        self.details_button.setObjectName("listItemButton")
        self.edit_button = QPushButton("Edit")
        self.edit_button.setObjectName("listItemButton")
        self.delete_button = QPushButton("Delete")
        self.delete_button.setObjectName("listItemButtonDelete")

        button_layout.addWidget(self.details_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        main_layout.addLayout(button_layout)

        self.setStyleSheet("""
            #habitListItem {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }
            #habitListItem:hover {
                background-color: #f8f9fa;
                border: 1px solid #cce5ff;
            }
            #listItemButton {
                font-size: 10px;
                padding: 6px 12px;
                background-color: transparent;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                color: #495057;
                font-weight: 500;
            }
            #listItemButton:hover {
                background-color: #f1f3f5;
                border-color: #007bff;
                color: #007bff;
            }
            #listItemButtonDelete {
                font-size: 10px;
                padding: 6px 12px;
                background-color: transparent;
                border: 1px solid #f1f3f5;
                border-radius: 5px;
                color: #fa5252;
                font-weight: 500;
            }
            #listItemButtonDelete:hover {
                background-color: #fa5252;
                color: white;
                border-color: #fa5252;
            }
        """)

    def update_display(self):
        """Update the widget with habit data."""
        self.name_label.setText(self.habit_data.get('name', 'N/A'))
        self.category_label.setText(self.habit_data.get('category', 'N/A'))

        start_date = format_date_for_display(self.habit_data.get('start_date', ''))
        self.date_label.setText(f"Started: {start_date}")

        # Update priority indicator color
        priority_color = get_priority_color(self.habit_data.get('priority', 'Medium'))
        self.priority_indicator.setStyleSheet(f"background-color: {priority_color}; border-radius: 2px;")

        # Update status label
        status = self.habit_data.get('status', 'Belum')
        status_color = get_status_color(status)
        self.status_label.setText(status)
        self.status_label.setStyleSheet(f"""
            background-color: transparent;
            color: {status_color};
            border: none;
            padding: 3px 0px;
            font-size: 11px;
            font-weight: bold;
        """)

    def setup_connections(self):
        """Connect signals to slots."""
        self.details_button.clicked.connect(lambda: self.details_clicked.emit(self.habit_id))
        self.edit_button.clicked.connect(lambda: self.edit_clicked.emit(self.habit_id))
        self.delete_button.clicked.connect(lambda: self.delete_clicked.emit(self.habit_id))

    def mouseDoubleClickEvent(self, event):
        """Handle double click to edit."""
        if event.button() == Qt.LeftButton:
            self.edit_clicked.emit(self.habit_id)
        super().mouseDoubleClickEvent(event)
