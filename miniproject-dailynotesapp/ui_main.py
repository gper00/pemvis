import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QCheckBox, QTextEdit,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox,
    QFrame, QSplitter, QDialog, QScrollArea
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtGui import QIcon, QColor, QFont
from style import STYLESHEET, CATEGORY_COLORS

class NoteDetailDialog(QDialog):
    def __init__(self, note, parent=None):
        super().__init__(parent)
        self.note = note
        self.parent = parent
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Note Details")
        self.setMinimumSize(600, 500)

        # Header section with title and metadata
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {CATEGORY_COLORS.get(self.note["category"], "#f5f5f5")};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(10)

        # Title with importance indicator
        title_text = "★ " + self.note["title"] if self.note["important"] else self.note["title"]
        title_label = QLabel(title_text)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        """)
        header_layout.addWidget(title_label)

        # Metadata in a horizontal layout
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(20)

        category_label = QLabel(f"📁 {self.note['category']}")
        created_label = QLabel(f"🕒 Created: {self.note['created_at']}")

        for label in [category_label, created_label]:
            label.setStyleSheet("""
                color: #34495e;
                font-size: 13px;
                font-weight: 500;
            """)
            meta_layout.addWidget(label)

        if 'updated_at' in self.note:
            updated_label = QLabel(f"🔄 Updated: {self.note['updated_at']}")
            updated_label.setStyleSheet("""
                color: #34495e;
                font-size: 13px;
                font-weight: 500;
            """)
            meta_layout.addWidget(updated_label)

        meta_layout.addStretch()
        header_layout.addLayout(meta_layout)
        self.main_layout.addWidget(header_frame)

        # Content area
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Content scroll area
        content_scroll = QScrollArea()
        content_scroll.setWidgetResizable(True)
        content_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        content_container = QWidget()
        content_container_layout = QVBoxLayout(content_container)

        content_label = QLabel(self.note["content"])
        content_label.setWordWrap(True)
        content_label.setStyleSheet("""
            font-size: 15px;
            color: #2c3e50;
            line-height: 1.6;
        """)

        content_container_layout.addWidget(content_label)
        content_container_layout.addStretch()

        content_scroll.setWidget(content_container)
        content_layout.addWidget(content_scroll)
        self.main_layout.addWidget(content_frame)

        # Create edit mode widgets (initially hidden)
        self.create_edit_widgets()
        self.edit_widget.hide()

        # Button layout at bottom
        self.button_frame = QFrame()
        self.button_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-top: 1px solid #e0e0e0;
                border-radius: 0px;
            }
        """)
        button_layout = QHBoxLayout(self.button_frame)
        button_layout.setContentsMargins(15, 15, 15, 15)
        button_layout.addStretch()

        self.edit_button = QPushButton("Edit")
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.edit_button.clicked.connect(self.toggle_edit_mode)

        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.close_button.clicked.connect(self.accept)

        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.close_button)
        self.main_layout.addWidget(self.button_frame)

    def create_edit_widgets(self):
        self.edit_widget = QWidget()
        edit_layout = QVBoxLayout(self.edit_widget)
        edit_layout.setSpacing(15)

        # Title input
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        title_layout = QHBoxLayout(title_frame)
        title_label = QLabel("Title:")
        title_label.setStyleSheet("font-weight: bold;")
        self.title_input = QLineEdit(self.note["title"])
        self.title_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        edit_layout.addWidget(title_frame)

        # Category and Important
        options_frame = QFrame()
        options_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        options_layout = QHBoxLayout(options_frame)

        category_label = QLabel("Category:")
        category_label.setStyleSheet("font-weight: bold;")
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Personal", "Work", "School"])
        self.category_combo.setCurrentText(self.note["category"])
        self.category_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 14px;
            }
        """)

        self.important_check = QCheckBox("Mark as Important")
        self.important_check.setChecked(self.note["important"])
        self.important_check.setStyleSheet("""
            QCheckBox {
                font-weight: bold;
                color: #e74c3c;
            }
        """)

        options_layout.addWidget(category_label)
        options_layout.addWidget(self.category_combo)
        options_layout.addStretch()
        options_layout.addWidget(self.important_check)
        edit_layout.addWidget(options_frame)

        # Content
        content_label = QLabel("Content:")
        content_label.setStyleSheet("font-weight: bold;")
        edit_layout.addWidget(content_label)

        self.content_text = QTextEdit()
        self.content_text.setText(self.note["content"])
        self.content_text.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        edit_layout.addWidget(self.content_text)

        self.main_layout.addWidget(self.edit_widget)

    def toggle_edit_mode(self):
        if self.edit_widget.isVisible():
            # Save changes
            if self.save_changes():
                self.edit_widget.hide()
                self.edit_button.setText("Edit")
                # Recreate view widgets with updated content
                for i in reversed(range(self.main_layout.count())):
                    widget = self.main_layout.itemAt(i).widget()
                    if widget != self.edit_widget and widget != self.button_frame:
                        widget.setParent(None)
                self.init_ui()
        else:
            # Switch to edit mode
            self.edit_widget.show()
            self.edit_button.setText("Save")
            # Hide view widgets except button frame
            for i in reversed(range(self.main_layout.count())):
                widget = self.main_layout.itemAt(i).widget()
                if widget != self.edit_widget and widget != self.button_frame:
                    widget.hide()

    def save_changes(self):
        # Update note data
        self.note["title"] = self.title_input.text()
        self.note["category"] = self.category_combo.currentText()
        self.note["important"] = self.important_check.isChecked()
        self.note["content"] = self.content_text.toPlainText()
        self.note["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update the notes file
        try:
            with open('notes_data.json', 'r') as f:
                notes = json.load(f)

            # Find and update the note
            for i, note in enumerate(notes):
                if note["id"] == self.note["id"]:
                    notes[i] = self.note
                    break

            with open('notes_data.json', 'w') as f:
                json.dump(notes, f, indent=4)

            # Show success message
            QMessageBox.information(self, "Success", "Note updated successfully!")

            # Refresh the main window's note list
            if isinstance(self.parent, NotesMainWindow):
                self.parent.load_notes()

            return True

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save changes: {str(e)}")
            return False

class NotesMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_notes()

    def init_ui(self):
        # Set window propertieson
        self.setWindowTitle("Mini Project - Daily Notes App")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet(STYLESHEET)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Left panel - Input form
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.setSpacing(16)

        # Student info section
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.StyledPanel)
        info_frame.setObjectName("infoFrame")
        info_layout = QVBoxLayout(info_frame)

        self.label_info = QLabel("Nama: UMAM ALPARIZI\nNIM: F1D02310141")
        self.label_info.setObjectName("studentInfo")
        info_layout.addWidget(self.label_info)

        left_layout.addWidget(info_frame)

        # Title input
        title_layout = QHBoxLayout()
        title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter note title")
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        left_layout.addLayout(title_layout)

        # Category and Important checkbox
        category_layout = QHBoxLayout()
        category_label = QLabel("Category:")
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Personal", "Work", "School"])

        self.important_check = QCheckBox("Important")

        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        category_layout.addWidget(self.important_check)
        left_layout.addLayout(category_layout)

        # Note content
        content_label = QLabel("Content:")
        left_layout.addWidget(content_label)

        self.content_text = QTextEdit()
        self.content_text.setPlaceholderText("Write your note here...")
        left_layout.addWidget(self.content_text)

        # Save button
        self.save_button = QPushButton("Save Note")
        self.save_button.setObjectName("saveButton")
        self.save_button.clicked.connect(self.save_note)
        left_layout.addWidget(self.save_button)

        # Right panel - Notes list
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(16, 16, 16, 16)
        right_layout.setSpacing(16)

        # Notes list header
        list_header = QLabel("Your Notes")
        list_header.setObjectName("listHeader")
        right_layout.addWidget(list_header)

        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search notes...")
        self.search_input.textChanged.connect(self.filter_notes)
        right_layout.addWidget(self.search_input)

        # Filter by category
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Personal", "Work", "School"])
        self.filter_combo.currentTextChanged.connect(self.filter_notes)

        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        right_layout.addLayout(filter_layout)

        # Notes list
        self.notes_list = QListWidget()
        self.notes_list.setObjectName("notesList")
        self.notes_list.itemDoubleClicked.connect(self.show_note_details)
        right_layout.addWidget(self.notes_list)

        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 500])

    def save_note(self):
        title = self.title_input.text().strip()
        category = self.category_combo.currentText()
        is_important = self.important_check.isChecked()
        content = self.content_text.toPlainText().strip()

        # Basic validation
        if not title:
            QMessageBox.warning(self, "Input Error", "Please enter a title for your note.")
            return

        if not content:
            QMessageBox.warning(self, "Input Error", "Please enter content for your note.")
            return

        # Create note object
        note = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "title": title,
            "category": category,
            "important": is_important,
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save note to file
        try:
            with open('notes_data.json', 'r') as f:
                notes = json.load(f)

            notes.append(note)

            with open('notes_data.json', 'w') as f:
                json.dump(notes, f, indent=4)

            # Show success message
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Success")
            msg_box.setText("Note saved successfully!")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.exec_()

            # Clear form
            self.title_input.clear()
            self.content_text.clear()
            self.important_check.setChecked(False)

            # Refresh notes list
            self.load_notes()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save note: {str(e)}")

    def load_notes(self):
        try:
            with open('notes_data.json', 'r') as f:
                notes = json.load(f)

            self.all_notes = notes
            self.filter_notes()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load notes: {str(e)}")

    def filter_notes(self):
        self.notes_list.clear()

        search_text = self.search_input.text().lower()
        selected_category = self.filter_combo.currentText()

        for note in self.all_notes:
            # Apply filters
            if selected_category != "All" and note["category"] != selected_category:
                continue

            if search_text and search_text not in note["title"].lower() and search_text not in note["content"].lower():
                continue

            # Create list item
            item = QListWidgetItem()

            # Format note title with date and importance indicator
            display_text = f"{note['title']}"
            if note["important"]:
                display_text = f"★ {display_text}"

            display_text += f" ({note['created_at']})"
            item.setText(display_text)

            # Set tooltip with preview of content
            content_preview = note["content"]
            if len(content_preview) > 100:
                content_preview = content_preview[:100] + "..."
            item.setToolTip(f"Category: {note['category']}\n\n{content_preview}")

            # Set data for retrieving later
            item.setData(Qt.UserRole, note["id"])

            # Set background color based on category
            if note["category"] in CATEGORY_COLORS:
                item.setBackground(QColor(CATEGORY_COLORS[note["category"]]))

            # Add to list
            self.notes_list.addItem(item)

    def show_note_details(self, item):
        note_id = item.data(Qt.UserRole)

        # Find the note with matching ID
        selected_note = None
        for note in self.all_notes:
            if note["id"] == note_id:
                selected_note = note
                break

        if selected_note:
            dialog = NoteDetailDialog(selected_note, self)
            dialog.exec_()
