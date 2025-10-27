"""
Habit Card Component for displaying individual habits
"""

from typing import Dict, Any, Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QFrame, QMenu, QAction, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor

from config.constants import (
    PRIORITY_COLORS, STATUS_COLORS, DISPLAY_DATE_FORMAT
)
from utils.helpers import (
    format_date_for_display, get_priority_color, get_status_color,
    truncate_text, calculate_completion_rate
)

class HabitCard(QFrame):
    """Habit card widget for displaying habit information"""

    # Signals
    edit_clicked = pyqtSignal(int)  # habit_id
    delete_clicked = pyqtSignal(int)  # habit_id
    status_changed = pyqtSignal(int, str)  # habit_id, new_status
    details_clicked = pyqtSignal(int)  # habit_id

    def __init__(self, habit_data: Dict[str, Any], view_mode: str = 'full', parent=None):
        super().__init__(parent)
        self.habit_data = habit_data
        self.habit_id = habit_data.get('id')
        self.view_mode = view_mode

        # Allow card to expand horizontally but keep vertical size fixed for consistency
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.setup_ui()
        self.setup_styling()
        self.setup_connections()
        self.update_display()
        self.set_view_mode(self.view_mode)
        self.add_shadow()

    def add_shadow(self):
        """Add a shadow effect to the card."""
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(2)
        self.shadow.setColor(QColor(0, 0, 0, 25)) # 10% opacity
        self.setGraphicsEffect(self.shadow)
        self.shadow.setEnabled(False) # Disabled by default

    def setup_ui(self):
        """Setup the user interface"""
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(1)
        self.setMidLineWidth(0)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header section
        header_layout = QHBoxLayout()

        # Habit name and priority
        name_layout = QVBoxLayout()

        self.name_label = QLabel(self.habit_data.get('name', 'Unnamed Habit'))
        self.name_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.name_label.setWordWrap(True)
        self.name_label.setStyleSheet("color: #212529;")
        name_layout.addWidget(self.name_label)

        # Priority badge
        self.priority_label = QLabel(self.habit_data.get('priority', 'Medium'))
        self.priority_label.setAlignment(Qt.AlignCenter)
        self.priority_label.setMaximumWidth(80)
        self.priority_label.setMaximumHeight(24)
        self.priority_label.setFont(QFont("Segoe UI", 9, QFont.Medium))
        name_layout.addWidget(self.priority_label)

        header_layout.addLayout(name_layout)
        header_layout.addStretch()

        # Menu button
        self.menu_button = QPushButton("⋮")
        self.menu_button.setMaximumSize(32, 32)
        self.menu_button.setToolTip("More options")
        header_layout.addWidget(self.menu_button)

        main_layout.addLayout(header_layout)

        # Content section
        content_layout = QVBoxLayout()
        content_layout.setSpacing(8)

        # Category and frequency
        info_layout = QHBoxLayout()

        self.category_label = QLabel(f"📂 {self.habit_data.get('category', 'Unknown')}")
        self.category_label.setFont(QFont("Segoe UI", 10))
        self.category_label.setStyleSheet("color: #6c757d;")

        self.frequency_label = QLabel(f"🔄 {self.habit_data.get('frequency', 1)}x/week")
        self.frequency_label.setFont(QFont("Segoe UI", 10))
        self.frequency_label.setStyleSheet("color: #6c757d;")

        info_layout.addWidget(self.category_label)
        info_layout.addStretch()
        info_layout.addWidget(self.frequency_label)

        content_layout.addLayout(info_layout)

        # Start date
        start_date = format_date_for_display(self.habit_data.get('start_date', ''))
        self.date_label = QLabel(f"📅 Started: {start_date}")
        self.date_label.setFont(QFont("Segoe UI", 9))
        self.date_label.setStyleSheet("color: #6c757d;")
        content_layout.addWidget(self.date_label)

        # Status
        self.status_label = QLabel(self.habit_data.get('status', 'Belum'))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setMaximumHeight(28)
        self.status_label.setFont(QFont("Segoe UI", 10, QFont.Medium))
        content_layout.addWidget(self.status_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumHeight(6)
        self.progress_bar.setTextVisible(False)
        content_layout.addWidget(self.progress_bar)

        # Progress text
        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setFont(QFont("Segoe UI", 9))
        self.progress_label.setStyleSheet("color: #6c757d;")
        content_layout.addWidget(self.progress_label)

        # Notes preview
        notes = self.habit_data.get('notes', '')
        if notes:
            self.notes_label = QLabel(truncate_text(notes, 80))
            self.notes_label.setFont(QFont("Segoe UI", 9))
            self.notes_label.setStyleSheet("color: #6c757d; font-style: italic;")
            self.notes_label.setWordWrap(True)
            content_layout.addWidget(self.notes_label)

        main_layout.addLayout(content_layout)

        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(8)

        self.complete_button = QPushButton("Mark Complete")
        self.complete_button.setMinimumHeight(36)
        self.complete_button.setFont(QFont("Segoe UI", 10, QFont.Medium))

        self.edit_button = QPushButton("Edit")
        self.edit_button.setMinimumHeight(36)
        self.edit_button.setFont(QFont("Segoe UI", 10, QFont.Medium))

        self.details_button = QPushButton("Details")
        self.details_button.setMinimumHeight(36)
        self.details_button.setFont(QFont("Segoe UI", 10, QFont.Medium))

        action_layout.addWidget(self.complete_button)
        action_layout.addWidget(self.edit_button)
        action_layout.addWidget(self.details_button)

        self.action_buttons_widget = QWidget()
        self.action_buttons_widget.setLayout(action_layout)
        main_layout.addWidget(self.action_buttons_widget)

        self.setLayout(main_layout)

        # Setup context menu
        self.setup_context_menu()

    def setup_styling(self):
        """Setup modern, clean styling"""
        # Set priority-based border color
        priority = self.habit_data.get('priority', 'Medium')
        border_color = get_priority_color(priority)

        self.setStyleSheet(f"""
            HabitCard {{
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-left: 4px solid {border_color};
                border-radius: 8px;
                margin: 0px;
            }}

            HabitCard:hover {{
                border-color: #dee2e6;
            }}

            QPushButton {{
                background-color: #f8f9fa;
                color: #495057;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                font-weight: 500;
                padding: 8px 16px;
            }}

            QPushButton:hover {{
                background-color: #e9ecef;
                border-color: #adb5bd;
            }}

            QPushButton:pressed {{
                background-color: #dee2e6;
            }}

            QPushButton#completeButton {{
                background-color: #28a745;
                color: white;
                border-color: #28a745;
            }}

            QPushButton#completeButton:hover {{
                background-color: #218838;
                border-color: #1e7e34;
            }}

            QPushButton#editButton {{
                background-color: #007bff;
                color: white;
                border-color: #007bff;
            }}

            QPushButton#editButton:hover {{
                background-color: #0056b3;
                border-color: #004085;
            }}

            QPushButton#detailsButton {{
                background-color: #6c757d;
                color: white;
                border-color: #6c757d;
            }}

            QPushButton#detailsButton:hover {{
                background-color: #545b62;
                border-color: #3d4449;
            }}

            QPushButton#menuButton {{
                background-color: transparent;
                color: #6c757d;
                font-size: 18px;
                font-weight: bold;
                border: none;
                padding: 0;
                border-radius: 4px;
            }}

            QPushButton#menuButton:hover {{
                background-color: #f8f9fa;
                color: #495057;
            }}

            QProgressBar {{
                border: none;
                background-color: #e9ecef;
                border-radius: 3px;
            }}

            QProgressBar::chunk {{
                background-color: #28a745;
                border-radius: 3px;
                margin: 0px;
            }}
        """)

        # Set button object names for specific styling
        self.complete_button.setObjectName("completeButton")
        self.edit_button.setObjectName("editButton")
        self.details_button.setObjectName("detailsButton")
        self.menu_button.setObjectName("menuButton")

    def setup_connections(self):
        """Setup signal connections"""
        self.complete_button.clicked.connect(self.toggle_completion)
        self.edit_button.clicked.connect(self.edit_habit)
        self.details_button.clicked.connect(self.show_details)
        self.menu_button.clicked.connect(self.show_context_menu)

    def setup_context_menu(self):
        """Setup context menu"""
        self.context_menu = QMenu(self)

        # Edit action
        edit_action = QAction("Edit Habit", self)
        edit_action.triggered.connect(self.edit_habit)
        self.context_menu.addAction(edit_action)

        # Delete action
        delete_action = QAction("Delete Habit", self)
        delete_action.triggered.connect(self.delete_habit)
        self.context_menu.addAction(delete_action)

        self.context_menu.addSeparator()

        # Mark complete/incomplete action
        self.toggle_action = QAction("Mark Complete", self)
        self.toggle_action.triggered.connect(self.toggle_completion)
        self.context_menu.addAction(self.toggle_action)

        # Details action
        details_action = QAction("View Details", self)
        details_action.triggered.connect(self.show_details)
        self.context_menu.addAction(details_action)

    def update_display(self):
        """Update card display based on current data"""
        # Update name
        self.name_label.setText(self.habit_data.get('name', 'Unnamed Habit'))

        # Update priority badge
        priority = self.habit_data.get('priority', 'Medium')
        self.priority_label.setText(priority)
        priority_color = get_priority_color(priority)
        self.priority_label.setStyleSheet(f"""
            background-color: {priority_color};
            color: white;
            border-radius: 12px;
            padding: 4px 8px;
            font-size: 9px;
            font-weight: bold;
        """)

        # Update category and frequency
        self.category_label.setText(f"📂 {self.habit_data.get('category', 'Unknown')}")
        self.frequency_label.setText(f"🔄 {self.habit_data.get('frequency', 1)}x/week")

        # Update start date
        start_date = format_date_for_display(self.habit_data.get('start_date', ''))
        self.date_label.setText(f"📅 Started: {start_date}")

        # Update status
        status = self.habit_data.get('status', 'Belum')
        self.status_label.setText(status)
        status_color = get_status_color(status)
        self.status_label.setStyleSheet(f"""
            background-color: {status_color};
            color: white;
            border-radius: 14px;
            padding: 6px 12px;
            font-size: 10px;
            font-weight: bold;
        """)

        # Update progress
        self.update_progress()

        # Update button text based on status
        if status == 'Selesai':
            self.complete_button.setText("Mark Incomplete")
            self.toggle_action.setText("Mark Incomplete")
        else:
            self.complete_button.setText("Mark Complete")
            self.toggle_action.setText("Mark Complete")

    def update_progress(self):
        """Update progress bar and label"""
        total_completed = self.habit_data.get('total_completed', 0)
        target_weekly = self.habit_data.get('target_weekly', 1)

        # Calculate progress percentage
        if target_weekly > 0:
            progress = min((total_completed / target_weekly) * 100, 100)
        else:
            progress = 0

        self.progress_bar.setValue(int(progress))

        # Update progress label
        self.progress_label.setText(f"Completed: {total_completed}/{target_weekly} this week")

        # Update progress bar color based on completion
        if progress >= 100:
            self.progress_bar.setStyleSheet("""
                QProgressBar::chunk {
                    background-color: #28a745;
                }
            """)
        elif progress >= 50:
            self.progress_bar.setStyleSheet("""
                QProgressBar::chunk {
                    background-color: #ffc107;
                }
            """)
        else:
            self.progress_bar.setStyleSheet("""
                QProgressBar::chunk {
                    background-color: #dc3545;
                }
            """)

    def toggle_completion(self):
        """Toggle habit completion status"""
        current_status = self.habit_data.get('status', 'Belum')
        new_status = 'Selesai' if current_status == 'Belum' else 'Belum'

        self.status_changed.emit(self.habit_id, new_status)

    def edit_habit(self):
        """Emit edit signal"""
        self.edit_clicked.emit(self.habit_id)

    def delete_habit(self):
        """Emit delete signal"""
        self.delete_clicked.emit(self.habit_id)

    def show_details(self):
        """Emit details signal"""
        self.details_clicked.emit(self.habit_id)

    def show_context_menu(self):
        """Show context menu"""
        self.context_menu.exec_(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))

    def set_view_mode(self, mode: str):
        """Set the card's view mode ('full' or 'compact')."""
        self.view_mode = mode
        is_compact = (mode == 'compact')

        # Elements to hide in compact mode
        self.date_label.setVisible(not is_compact)
        self.progress_bar.setVisible(not is_compact)
        self.progress_label.setVisible(not is_compact)
        self.action_buttons_widget.setVisible(not is_compact)

        if hasattr(self, 'notes_label'):
            self.notes_label.setVisible(not is_compact)

        # Adjust layout for compact view
        if is_compact:
            self.name_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
            self.setMinimumHeight(0) # Reset min height
            self.setMaximumHeight(160) # Set max height for compact
        else:
            self.name_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
            self.setMaximumHeight(16777215) # Reset max height

        self.update()
        self.adjustSize()

    def update_habit_data(self, new_data: Dict[str, Any]):
        """Update habit data and refresh display"""
        self.habit_data.update(new_data)
        self.update_display()

    def set_highlighted(self, highlighted: bool):
        """Set card highlight state"""
        if highlighted:
            self.setStyleSheet(self.styleSheet() + """
                HabitCard {
                    background-color: #f8f9fa;
                    border-width: 2px;
                }
            """)
        else:
            self.setup_styling()

    def mousePressEvent(self, event):
        """Handle mouse press events"""
        if event.button() == Qt.LeftButton:
            # Single click to highlight
            self.set_highlighted(True)
        elif event.button() == Qt.RightButton:
            # Right click to show context menu
            self.show_context_menu()

        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        """Handle double click to edit"""
        if event.button() == Qt.LeftButton:
            self.edit_habit()

        super().mouseDoubleClickEvent(event)

    def enterEvent(self, event):
        """Show shadow on hover."""
        self.shadow.setEnabled(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Hide shadow when not hovering."""
        self.shadow.setEnabled(False)
        super().leaveEvent(event)
