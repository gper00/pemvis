from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor

class NoteItemWidget(QWidget):
    """Custom widget for displaying a note item with more styling options"""
    
    deleted = pyqtSignal(str)  # Signal emitted when delete button is clicked
    viewed = pyqtSignal(str)   # Signal emitted when view button is clicked
    
    def __init__(self, note, parent=None):
        super().__init__(parent)
        self.note = note
        self.note_id = note["id"]
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Note container frame
        container = QFrame()
        container.setFrameShape(QFrame.StyledPanel)
        container.setObjectName("noteItemFrame")
        
        # Get background color based on category
        category_colors = {
            "Personal": "#e3f2fd",  # Light blue
            "Work": "#e8f5e9",      # Light green
            "School": "#f3e5f5"     # Light purple
        }
        
        bg_color = category_colors.get(self.note["category"], "#f5f5f5")
        container.setStyleSheet(f"background-color: {bg_color}; border-radius: 5px;")
        
        # Container layout
        container_layout = QVBoxLayout(container)
        
        # Title with importance indicator
        title_text = self.note["title"]
        if self.note["important"]:
            title_text = f"★ {title_text}"
            
        title_label = QLabel(title_text)
        title_label.setObjectName("noteTitle")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        container_layout.addWidget(title_label)
        
        # Metadata
        meta_layout = QHBoxLayout()
        category_label = QLabel(f"Category: {self.note['category']}")
        date_label = QLabel(self.note["created_at"])
        date_label.setAlignment(Qt.AlignRight)
        
        meta_layout.addWidget(category_label)
        meta_layout.addWidget(date_label)
        container_layout.addLayout(meta_layout)
        
        # Content preview
        content_preview = self.note["content"]
        if len(content_preview) > 100:
            content_preview = content_preview[:100] + "..."
            
        content_label = QLabel(content_preview)
        content_label.setWordWrap(True)
        container_layout.addWidget(content_label)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        view_btn = QPushButton("View")
        view_btn.setObjectName("viewButton")
        view_btn.clicked.connect(lambda: self.viewed.emit(self.note_id))
        
        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("deleteButton")
        delete_btn.clicked.connect(lambda: self.deleted.emit(self.note_id))
        
        btn_layout.addWidget(view_btn)
        btn_layout.addWidget(delete_btn)
        container_layout.addLayout(btn_layout)
        
        # Add the container to the main layout
        layout.addWidget(container)