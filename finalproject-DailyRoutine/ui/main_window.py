"""
Main Window for DailyRoutine application
"""

import sys
from typing import List, Dict, Any, Optional
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea,
    QMenuBar, QStatusBar, QMessageBox, QGroupBox, QProgressBar, QAction,
    QFrame, QSpacerItem, QSizePolicy, QGridLayout, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap

from config.constants import APP_NAME, AUTHOR, NIM, HABIT_CATEGORIES, HABIT_STATUS
from database.database import db_manager
from utils.export_utils import export_manager
from .habit_dialog import HabitDialog
from .habit_card import HabitCard
from .habit_details_dialog import HabitDetailsDialog
from .habit_list_item import HabitListItem
from utils.helpers import format_date_for_display, get_priority_color, get_status_color

class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.habits = []
        self.filtered_habits = []

        self.setup_ui()
        self.setup_menu_bar()
        self.setup_status_bar()
        self.setup_styling()
        self.setup_connections()
        self.load_habits()

    def add_shadow_effect(self, widget):
        """Apply a standard shadow effect to a widget."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(1)
        shadow.setColor(QColor(0, 0, 0, 30)) # 12% opacity
        widget.setGraphicsEffect(shadow)

    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1000, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # View mode state
        self.current_view_mode = 'list' # Default to list view

        # Toolbar
        self.setup_toolbar(main_layout)

        # Filters
        self.setup_filters(main_layout)

        # Content area
        self.setup_content_area(main_layout)

    def setup_toolbar(self, parent_layout):
        """Setup toolbar"""
        toolbar_frame = QFrame()
        toolbar_frame.setObjectName("toolbar")
        toolbar_layout = QHBoxLayout(toolbar_frame)
        toolbar_layout.setContentsMargins(20, 15, 20, 15)
        toolbar_layout.setSpacing(15)

        # Add new habit button
        self.add_button = QPushButton("+ Add New Habit")
        self.add_button.setObjectName("primaryButton")
        self.add_button.setMinimumHeight(45)
        self.add_button.setFont(QFont("Segoe UI", 11, QFont.Medium))
        toolbar_layout.addWidget(self.add_button)

        # Spacer
        toolbar_layout.addSpacing(20)

        # Search box
        search_frame = QFrame()
        search_frame.setObjectName("searchFrame")
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(15, 0, 15, 0)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search habits...")
        self.search_box.setObjectName("searchBox")
        self.search_box.setMinimumHeight(45)
        self.search_box.setFont(QFont("Segoe UI", 10))
        search_layout.addWidget(self.search_box)

        toolbar_layout.addWidget(search_frame)
        toolbar_layout.addStretch()

        # Action buttons
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setObjectName("outlineButton")
        self.refresh_button.setMinimumHeight(45)
        self.refresh_button.setFont(QFont("Segoe UI", 10))
        toolbar_layout.addWidget(self.refresh_button)

        self.export_button = QPushButton("Export")
        self.export_button.setObjectName("secondaryButton")
        self.export_button.setMinimumHeight(45)
        self.export_button.setFont(QFont("Segoe UI", 10))
        toolbar_layout.addWidget(self.export_button)

        parent_layout.addWidget(toolbar_frame)

    def setup_filters(self, parent_layout):
        """Setup filters"""
        filter_frame = QFrame()
        filter_frame.setObjectName("filterFrame")
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(20, 15, 20, 15)
        filter_layout.setSpacing(15)

        # Filter labels and combos
        filter_layout.addWidget(QLabel("Category:"))

        self.category_filter = QComboBox()
        self.category_filter.setObjectName("filterCombo")
        self.category_filter.addItem("All Categories")
        self.category_filter.addItems(HABIT_CATEGORIES)
        self.category_filter.setMinimumHeight(40)
        self.category_filter.setFont(QFont("Segoe UI", 10))
        filter_layout.addWidget(self.category_filter)

        filter_layout.addSpacing(20)
        filter_layout.addWidget(QLabel("Status:"))

        self.status_filter = QComboBox()
        self.status_filter.setObjectName("filterCombo")
        self.status_filter.addItem("All Status")
        self.status_filter.addItems(HABIT_STATUS)
        self.status_filter.setMinimumHeight(40)
        self.status_filter.setFont(QFont("Segoe UI", 10))
        filter_layout.addWidget(self.status_filter)

        filter_layout.addStretch()

        self.clear_filters_button = QPushButton("Clear Filters")
        self.clear_filters_button.setObjectName("textButton")
        self.clear_filters_button.setMinimumHeight(40)
        self.clear_filters_button.setFont(QFont("Segoe UI", 10))
        filter_layout.addWidget(self.clear_filters_button)

        parent_layout.addWidget(filter_frame)

    def setup_content_area(self, parent_layout):
        """Setup content area with habit list and statistics"""
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QHBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 0, 20, 20)
        content_layout.setSpacing(20)

        # Left side - Habit list (70%)
        habit_list_frame = QFrame()
        habit_list_frame.setObjectName("habitListFrame")
        habit_list_layout = QVBoxLayout(habit_list_frame)
        habit_list_layout.setContentsMargins(0, 0, 0, 0)
        habit_list_layout.setSpacing(0)

        # Habit list header
        header_frame = QFrame()
        header_frame.setObjectName("listHeader")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)

        title_label = QLabel("My Habits")
        title_label.setObjectName("sectionTitle")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # View mode buttons
        self.view_mode_buttons = QHBoxLayout()
        self.grid_view_button = QPushButton("Grid") # Placeholder, will use icon later
        self.grid_view_button.setObjectName("viewModeButton")
        self.list_view_button = QPushButton("List") # Placeholder, will use icon later
        self.list_view_button.setObjectName("viewModeButton")
        self.list_view_button.setProperty("active", True) # Default view is list
        self.view_mode_buttons.addWidget(self.grid_view_button)
        self.view_mode_buttons.addWidget(self.list_view_button)
        header_layout.addLayout(self.view_mode_buttons)

        header_layout.addSpacing(15)

        # Habit count
        self.habit_count_label = QLabel("0 habits")
        self.habit_count_label.setObjectName("countLabel")
        self.habit_count_label.setFont(QFont("Segoe UI", 12))
        header_layout.addWidget(self.habit_count_label)

        habit_list_layout.addWidget(header_frame)

        # Scroll area for habit cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("scrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Container widget
        self.habit_container = QWidget()
        self.habit_container.setObjectName("habitContainer")

        # We will set the layout in update_habits_view
        self.habit_layout = None

        self.scroll_area.setWidget(self.habit_container)
        habit_list_layout.addWidget(self.scroll_area)

        content_layout.addWidget(habit_list_frame, 7)  # 70% width

        # Right side - Statistics (30%)
        stats_frame = QFrame()
        stats_frame.setObjectName("statsFrame")
        stats_layout = QVBoxLayout(stats_frame)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(0)

        # Stats header
        stats_header = QFrame()
        stats_header.setObjectName("statsHeader")
        stats_header_layout = QHBoxLayout(stats_header)
        stats_header_layout.setContentsMargins(20, 15, 20, 15)

        stats_title = QLabel("Statistics")
        stats_title.setObjectName("sectionTitle")
        stats_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        stats_header_layout.addWidget(stats_title)

        stats_layout.addWidget(stats_header)

        # Stats content
        stats_content = QFrame()
        stats_content.setObjectName("statsContent")
        stats_content_layout = QVBoxLayout(stats_content)
        stats_content_layout.setContentsMargins(20, 20, 20, 20)
        stats_content_layout.setSpacing(20)

        # Summary cards
        self.setup_summary_cards(stats_content_layout)

        # Progress section
        self.setup_progress_section(stats_content_layout)

        # Category breakdown
        self.setup_category_breakdown(stats_content_layout)

        stats_content_layout.addStretch()
        stats_layout.addWidget(stats_content)

        content_layout.addWidget(stats_frame, 3)  # 30% width

        parent_layout.addWidget(content_frame)

    def setup_summary_cards(self, parent_layout):
        """Setup summary statistics cards in a horizontal layout"""
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(20)

        # Total habits card
        total_card = QFrame()
        total_card.setObjectName("statCard")
        total_layout = QVBoxLayout(total_card)
        total_layout.setContentsMargins(20, 15, 20, 15)

        total_title = QLabel("Total Habits")
        total_title.setObjectName("statTitle")
        total_title.setFont(QFont("Segoe UI", 11))
        total_layout.addWidget(total_title)

        self.total_label = QLabel("0")
        self.total_label.setObjectName("statValue")
        self.total_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.total_label.setAlignment(Qt.AlignCenter)
        total_layout.addWidget(self.total_label)

        summary_layout.addWidget(total_card)

        # Completion rate card
        completion_card = QFrame()
        completion_card.setObjectName("statCard")
        completion_layout = QVBoxLayout(completion_card)
        completion_layout.setContentsMargins(20, 15, 20, 15)

        completion_title = QLabel("Completion Rate")
        completion_title.setObjectName("statTitle")
        completion_title.setFont(QFont("Segoe UI", 11))
        completion_layout.addWidget(completion_title)

        self.completion_rate_label = QLabel("0.0%")
        self.completion_rate_label.setObjectName("statValue")
        self.completion_rate_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.completion_rate_label.setAlignment(Qt.AlignCenter)
        completion_layout.addWidget(self.completion_rate_label)

        summary_layout.addWidget(completion_card)
        parent_layout.addLayout(summary_layout)

        # Apply shadows
        self.add_shadow_effect(total_card)
        self.add_shadow_effect(completion_card)

    def setup_progress_section(self, parent_layout):
        """Setup progress section"""
        progress_frame = QFrame()
        progress_frame.setObjectName("statCard")
        progress_layout = QVBoxLayout(progress_frame)
        progress_layout.setContentsMargins(20, 15, 20, 15)
        progress_layout.setSpacing(10)

        progress_title = QLabel("Weekly Progress")
        progress_title.setObjectName("statTitle")
        progress_title.setFont(QFont("Segoe UI", 11))
        progress_layout.addWidget(progress_title)

        # Progress bar
        self.completion_progress = QProgressBar()
        self.completion_progress.setObjectName("progressBar")
        self.completion_progress.setMaximumHeight(6)
        self.completion_progress.setTextVisible(False)
        progress_layout.addWidget(self.completion_progress)

        # Container for progress labels
        labels_widget = QWidget()
        progress_labels_layout = QHBoxLayout(labels_widget)
        progress_labels_layout.setContentsMargins(0, 5, 0, 0)
        progress_labels_layout.setSpacing(5)

        self.completed_label = QLabel("Completed: 0")
        self.completed_label.setObjectName("progressLabel")
        self.completed_label.setFont(QFont("Segoe UI", 9))
        progress_labels_layout.addWidget(self.completed_label)

        progress_labels_layout.addStretch()

        self.pending_label = QLabel("Pending: 0")
        self.pending_label.setObjectName("progressLabel")
        self.pending_label.setFont(QFont("Segoe UI", 9))
        progress_labels_layout.addWidget(self.pending_label)

        progress_layout.addWidget(labels_widget)
        parent_layout.addWidget(progress_frame)
        self.add_shadow_effect(progress_frame)

    def setup_category_breakdown(self, parent_layout):
        """Setup category breakdown"""
        category_frame = QFrame()
        category_frame.setObjectName("statCard")
        category_layout = QVBoxLayout(category_frame)
        category_layout.setContentsMargins(20, 15, 20, 20)
        category_layout.setSpacing(10) # Adjusted spacing

        category_title = QLabel("By Category")
        category_title.setObjectName("statTitle")
        category_title.setFont(QFont("Segoe UI", 11))
        category_layout.addWidget(category_title)

        # Category labels layout
        self.category_grid_layout = QVBoxLayout()
        self.category_grid_layout.setSpacing(10) # Adjusted spacing
        category_layout.addLayout(self.category_grid_layout)

        self.category_labels = {}
        for category in HABIT_CATEGORIES:
            label = QLabel(f"{category}: 0")
            label.setObjectName("categoryLabel")
            label.setFont(QFont("Segoe UI", 10))
            label.setMinimumHeight(22) # Ensure enough height for the font
            self.category_labels[category] = label
            self.category_grid_layout.addWidget(label)

        category_layout.addStretch()
        parent_layout.addWidget(category_frame)
        self.add_shadow_effect(category_frame)

    def setup_menu_bar(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        menubar.setObjectName("menuBar")

        # File menu
        file_menu = menubar.addMenu('File')

        new_action = QAction('New Habit', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.add_new_habit)
        file_menu.addAction(new_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Export menu
        export_menu = menubar.addMenu('Export')

        pdf_action = QAction('Export to PDF', self)
        pdf_action.setShortcut('Ctrl+P')
        pdf_action.triggered.connect(lambda: self.export_data('pdf'))
        export_menu.addAction(pdf_action)

        csv_action = QAction('Export to CSV', self)
        csv_action.setShortcut('Ctrl+E')
        csv_action.triggered.connect(lambda: self.export_data('csv'))
        export_menu.addAction(csv_action)

        # Help menu
        help_menu = menubar.addMenu('Help')

        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_status_bar(self):
        """Setup status bar"""
        status_bar = self.statusBar()
        status_bar.setObjectName("statusBar")

        # Student info on the left
        student_info_label = QLabel(f"Nama: {AUTHOR} | NIM: {NIM}")
        student_info_label.setObjectName("statusLabel")
        status_bar.addWidget(student_info_label)

        # Dynamic info on the right
        self.status_dynamic_label = QLabel("Ready")
        self.status_dynamic_label.setObjectName("statusLabel")
        status_bar.addPermanentWidget(self.status_dynamic_label)

    def setup_styling(self):
        """Setup modern, clean styling"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }

            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e9ecef;
                color: #495057;
                font-weight: 500;
                padding: 8px;
            }

            QMenuBar::item:selected {
                background-color: #e9ecef;
                border-radius: 4px;
            }

            QStatusBar {
                background-color: #ffffff;
                color: #6c757d;
                border-top: 1px solid #e9ecef;
                padding: 8px 20px;
                font-size: 11px;
            }

            #toolbar {
                background-color: #ffffff;
                border-bottom: 1px solid #e9ecef;
            }

            #filterFrame {
                background-color: #ffffff;
                border-bottom: none;
            }

            #contentFrame {
                background-color: #f8f9fa;
            }

            #habitListFrame {
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #e9ecef;
            }

            #listHeader {
                background-color: #f8f9fa;
                border-bottom: 1px solid #e9ecef;
                border-radius: 8px 8px 0 0;
            }

            #sectionTitle {
                color: #212529;
            }

            #countLabel {
                color: #6c757d;
            }

            #scrollArea {
                border: none;
                background-color: transparent;
            }

            #scrollArea QScrollBar:vertical {
                background-color: #f8f9fa;
                width: 8px;
                border-radius: 4px;
            }

            #scrollArea QScrollBar::handle:vertical {
                background-color: #dee2e6;
                border-radius: 4px;
                min-height: 20px;
            }

            #scrollArea QScrollBar::handle:vertical:hover {
                background-color: #adb5bd;
            }

            #habitContainer {
                background-color: transparent;
            }

            #statsFrame {
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #e9ecef;
            }

            #statsHeader {
                background-color: #f8f9fa;
                border-bottom: 1px solid #e9ecef;
                border-radius: 8px 8px 0 0;
            }

            #statsContent {
                background-color: transparent;
            }

            #statCard {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }

            #statTitle {
                color: #6c757d;
                font-weight: 500;
            }

            #statValue {
                color: #212529;
            }

            #progressFrame {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }

            #sectionSubtitle {
                color: #212529;
            }

            #progressBar {
                border: none;
                background-color: #e9ecef;
                border-radius: 4px;
            }

            #progressBar::chunk {
                background-color: #007bff;
                border-radius: 4px;
            }

            #progressLabel {
                color: #6c757d;
            }

            #categoryFrame {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }

            #categoryLabel {
                color: #495057;
            }

            #viewModeButton {
                background-color: transparent;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 10px;
                font-weight: 500;
                color: #6c757d;
            }

            #viewModeButton:hover {
                background-color: #f8f9fa;
            }

            #viewModeButton[active="true"] {
                background-color: #007bff;
                color: white;
                border-color: #007bff;
            }

            #searchFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }

            #searchBox {
                border: none;
                background-color: transparent;
                color: #495057;
                font-size: 14px;
            }

            #searchBox:focus {
                border: none;
            }

            #filterCombo {
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: #ffffff;
                color: #495057;
                min-width: 120px;
            }

            #filterCombo::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: #e9ecef;
                border-left-style: solid;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }

            #filterCombo::down-arrow {
                image: url(assets/icons/chevron-down.svg);
                width: 16px;
                height: 16px;
            }

            #filterCombo:focus {
                border-color: #007bff;
            }

            #primaryButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 500;
                padding: 12px 24px;
            }

            #primaryButton:hover {
                background-color: #0056b3;
            }

            #primaryButton:pressed {
                background-color: #004085;
            }

            #secondaryButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 500;
                padding: 12px 24px;
            }

            #secondaryButton:hover {
                background-color: #545b62;
            }

            #secondaryButton:pressed {
                background-color: #3d4449;
            }

            #outlineButton {
                background-color: transparent;
                color: #6c757d;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                font-weight: 500;
                padding: 12px 24px;
            }

            #outlineButton:hover {
                background-color: #f8f9fa;
                color: #212529;
                border-color: #adb5bd;
            }

            #textButton {
                background-color: transparent;
                color: #007bff;
                border: none;
                font-weight: 500;
                padding: 8px 16px;
            }

            #textButton:hover {
                background-color: #f8f9fa;
                border-radius: 6px;
            }

            QLabel {
                color: #495057;
            }
        """)

    def setup_connections(self):
        """Setup signal connections"""
        self.add_button.clicked.connect(self.add_new_habit)
        self.refresh_button.clicked.connect(self.refresh_habits)
        self.export_button.clicked.connect(lambda: self.export_data('pdf'))
        self.clear_filters_button.clicked.connect(self.clear_filters)

        self.category_filter.currentTextChanged.connect(self.apply_filters)
        self.status_filter.currentTextChanged.connect(self.apply_filters)
        self.search_box.textChanged.connect(self.apply_filters)

        # View mode connections
        self.grid_view_button.clicked.connect(lambda: self.set_view_mode('grid'))
        self.list_view_button.clicked.connect(lambda: self.set_view_mode('list'))

    def load_habits(self):
        """Load habits from database"""
        try:
            self.habits = db_manager.get_all_habits()
            self.filtered_habits = self.habits.copy()
            self.update_habits_view()
            self.update_statistics()
            print(f"Loaded {len(self.habits)} habits")
        except Exception as e:
            print(f"Error loading habits: {e}")
            QMessageBox.critical(self, "Error", f"Error loading habits: {e}")

    def update_habits_view(self):
        """Refresh the habits display based on the current view mode."""
        # Clear existing widgets and layout
        if self.habit_layout is not None:
            while self.habit_layout.count():
                child = self.habit_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            QWidget().setLayout(self.habit_layout)

        # Create new layout based on view mode
        if self.current_view_mode == 'grid':
            self.habit_layout = QGridLayout()
            self.habit_layout.setSpacing(20)
            self.habit_layout.setContentsMargins(20, 20, 20, 20)

            row, col = 0, 0
            num_columns = 3
            for habit in self.filtered_habits:
                card = HabitCard(habit, view_mode='compact', parent=self)
                card.edit_clicked.connect(self.edit_habit)
                card.delete_clicked.connect(self.delete_habit)
                card.status_changed.connect(self.change_habit_status)
                card.details_clicked.connect(self.show_habit_details)
                self.habit_layout.addWidget(card, row, col)
                col += 1
                if col >= num_columns:
                    col = 0
                    row += 1

            # Make columns stretchable to fill width
            for i in range(num_columns):
                self.habit_layout.setColumnStretch(i, 1)

            # Add a row stretch to push cards to the top
            self.habit_layout.setRowStretch(row + 1, 1)

        else:  # list view
            self.habit_layout = QVBoxLayout()
            self.habit_layout.setSpacing(10)
            self.habit_layout.setContentsMargins(15, 15, 15, 15)

            for habit in self.filtered_habits:
                list_item = HabitListItem(habit, parent=self)
                list_item.edit_clicked.connect(self.edit_habit)
                list_item.delete_clicked.connect(self.delete_habit)
                list_item.status_changed.connect(self.change_habit_status)
                list_item.details_clicked.connect(self.show_habit_details)
                self.habit_layout.addWidget(list_item)

            self.habit_layout.addStretch(1)

        self.habit_container.setLayout(self.habit_layout)
        self.update_habit_count()

    def apply_filters(self):
        """Apply filters to habit list"""
        filters = {}

        category = self.category_filter.currentText()
        if category != "All Categories":
            filters['category'] = category

        status = self.status_filter.currentText()
        if status != "All Status":
            filters['status'] = status

        search_text = self.search_box.text().strip()
        if search_text:
            filters['search'] = search_text

        try:
            self.filtered_habits = db_manager.get_all_habits(filters)
            self.update_habits_view()
            self.update_habit_count()
        except Exception as e:
            print(f"Error applying filters: {e}")

    def clear_filters(self):
        """Clear all filters"""
        self.category_filter.setCurrentText("All Categories")
        self.status_filter.setCurrentText("All Status")
        self.search_box.clear()
        self.category_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)
        self.apply_filters()

    def set_view_mode(self, mode):
        """Set the view mode for habits (grid or list)."""
        if self.current_view_mode == mode:
            return

        self.current_view_mode = mode
        self.grid_view_button.setProperty("active", mode == 'grid')
        self.list_view_button.setProperty("active", mode == 'list')

        # Re-apply stylesheet to update button appearances
        self.grid_view_button.style().unpolish(self.grid_view_button)
        self.grid_view_button.style().polish(self.grid_view_button)
        self.list_view_button.style().unpolish(self.list_view_button)
        self.list_view_button.style().polish(self.list_view_button)

        self.update_habits_view()

    def add_new_habit(self):
        """Show dialog to add new habit"""
        dialog = HabitDialog(self)
        dialog.habit_saved.connect(self.save_new_habit)
        dialog.exec_()

    def save_new_habit(self, habit_data):
        """Save new habit"""
        try:
            habit_id = db_manager.create_habit(habit_data)
            self.load_habits()
            self.apply_filters()
            QMessageBox.information(self, "Success", "Habit created successfully!")
        except Exception as e:
            print(f"Error saving habit: {e}")
            QMessageBox.critical(self, "Error", f"Error saving habit: {e}")

    def edit_habit(self, habit_id):
        """Edit habit"""
        try:
            habit_data = db_manager.get_habit(habit_id)
            if habit_data:
                dialog = HabitDialog(self, habit_data)
                dialog.habit_saved.connect(lambda data: self.update_habit(habit_id, data))
                dialog.exec_()
        except Exception as e:
            print(f"Error editing habit: {e}")
            QMessageBox.critical(self, "Error", f"Error editing habit: {e}")

    def update_habit(self, habit_id, habit_data):
        """Update habit"""
        try:
            success = db_manager.update_habit(habit_id, habit_data)
            if success:
                self.load_habits()
                self.apply_filters()
                QMessageBox.information(self, "Success", "Habit updated successfully!")
        except Exception as e:
            print(f"Error updating habit: {e}")
            QMessageBox.critical(self, "Error", f"Error updating habit: {e}")

    def delete_habit(self, habit_id):
        """Delete habit"""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this habit?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                success = db_manager.delete_habit(habit_id)
                if success:
                    self.load_habits()
                    self.apply_filters()
                    QMessageBox.information(self, "Success", "Habit deleted successfully!")
            except Exception as e:
                print(f"Error deleting habit: {e}")
                QMessageBox.critical(self, "Error", f"Error deleting habit: {e}")

    def change_habit_status(self, habit_id, new_status):
        """Change habit status"""
        try:
            habit_data = db_manager.get_habit(habit_id)
            if habit_data:
                habit_data['status'] = new_status
                db_manager.update_habit(habit_id, habit_data)
                self.load_habits()
                self.apply_filters()
        except Exception as e:
            print(f"Error changing status: {e}")

    def show_habit_details(self, habit_id: int):
        """Show habit details in a detailed dialog"""
        try:
            habit_data = db_manager.get_habit(habit_id)
            if habit_data:
                dialog = HabitDetailsDialog(habit_data, self)
                dialog.status_change_requested.connect(self.change_habit_status)
                dialog.exec_()
            else:
                QMessageBox.warning(self, "Error", "Habit not found!")

        except Exception as e:
            print(f"Error showing habit details: {e}")
            QMessageBox.critical(self, "Error", f"Error showing habit details: {e}")

    def refresh_habits(self):
        """Refresh habits"""
        self.load_habits()
        self.apply_filters()
        QMessageBox.information(self, "Success", "Habits refreshed!")

    def export_data(self, format_type):
        """Export data"""
        try:
            if format_type == 'pdf':
                filepath = export_manager.export_to_pdf(self.filtered_habits)
            else:
                filepath = export_manager.export_to_csv(self.filtered_habits)

            QMessageBox.information(self, "Success", f"Exported to {filepath}")
        except Exception as e:
            print(f"Error exporting: {e}")
            QMessageBox.critical(self, "Error", f"Error exporting: {e}")

    def update_statistics(self):
        """Update statistics"""
        total = len(self.habits)
        completed = sum(1 for h in self.habits if h.get('status') == 'Selesai')
        pending = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0

        # Update main statistics
        self.total_label.setText(str(total))
        self.completed_label.setText(f"Completed: {completed}")
        self.pending_label.setText(f"Pending: {pending}")
        self.completion_rate_label.setText(f"{completion_rate:.1f}%")

        # Update progress bar
        self.completion_progress.setValue(int(completion_rate))

        # Update category breakdown
        self.update_category_breakdown()

        self.update_habit_count()

    def update_category_breakdown(self):
        """Update the category breakdown in the statistics panel."""
        category_count = {cat: 0 for cat in HABIT_CATEGORIES}
        for habit in self.habits:
            category = habit.get('category', 'Unknown')
            if category in category_count:
                category_count[category] += 1

        for category, label in self.category_labels.items():
            count = category_count.get(category, 0)
            label.setText(f"∙ {category}: {count}")

    def update_habit_count(self):
        """Update habit count label"""
        count = len(self.filtered_habits)
        self.habit_count_label.setText(f"{count} habit{'s' if count != 1 else ''}")

    def show_about(self):
        """Show a custom styled about dialog."""
        dialog = QMessageBox(self)
        dialog.setWindowTitle("About")

        # Custom icon
        try:
            pixmap = QPixmap("assets/icons/lightbulb.svg").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            dialog.setIconPixmap(pixmap)
        except Exception as e:
            print(f"Could not load about icon: {e}")

        about_text = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; text-align: center; margin-left: 20px;">
            <h2 style="color: #212529; margin:0; padding-bottom: 5px;">{APP_NAME}</h2>
            <p style="color: #6c757d; margin:0; padding-bottom: 25px;">Habit Tracking Application</p>

            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: left; border: 1px solid #e9ecef;">
                <p><strong>Developer:</strong> &nbsp; {AUTHOR}</p>
                <p><strong>NIM:</strong> &nbsp; {NIM}</p>
                <p><strong>Version:</strong> &nbsp; 1.0.0</p>
            </div>

            <p style="color: #6c757d; font-size: 11px; margin-top: 25px;">
                Built with PyQt5 for Visual Programming Course
            </p>
        </div>
        """
        dialog.setText(about_text)

        # Style the OK button
        ok_button = dialog.addButton(QMessageBox.Ok)
        ok_button.setMinimumWidth(100)
        dialog.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QLabel {
                color: #495057;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 500;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        dialog.exec_()

    def closeEvent(self, event):
        """Handle close event"""
        reply = QMessageBox.question(
            self, "Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
