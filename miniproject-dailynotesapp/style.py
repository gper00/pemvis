CATEGORY_COLORS = {
    "Personal": "#e3f2fd",  # Light blue
    "Work": "#e8f5e9",     # Light green
    "School": "#f3e5f5"    # Light purple
}

STYLESHEET = """
QMainWindow {
    background-color: #f5f5f5;
}

QLabel {
    font-size: 12px;
    color: #424242;
}

QLabel#studentInfo {
    font-weight: bold; 
    color: #1565c0; 
    background-color: #e3f2fd; 
    padding: 10px;
    border-radius: 5px;
    font-size: 14px;
}

QLabel#listHeader {
    font-size: 18px;
    font-weight: bold;
    color: #1565c0;
    padding-bottom: 8px;
}

QLineEdit, QTextEdit, QComboBox {
    border: 1px solid #bdbdbd;
    border-radius: 4px;
    padding: 8px;
    background-color: white;
    selection-background-color: #bbdefb;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid #1976d2;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 24px;
    border-left: 1px solid #bdbdbd;
}

QPushButton {
    background-color: #1976d2;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1565c0;
}

QPushButton:pressed {
    background-color: #0d47a1;
}

QPushButton#saveButton {
    font-size: 14px;
    padding: 10px 20px;
}

QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #bdbdbd;
    border-radius: 3px;
    background-color: white;
}

QCheckBox::indicator:checked {
    background-color: #1976d2;
    border: 1px solid #1976d2;
}

QListWidget {
    border: 1px solid #bdbdbd;
    border-radius: 4px;
    padding: 4px;
    background-color: white;
    alternate-background-color: #f5f5f5;
}

QListWidget::item {
    border-bottom: 1px solid #e0e0e0;
    padding: 8px 4px;
}

QListWidget::item:selected {
    background-color: #bbdefb;
    color: #0d47a1;
}

QListWidget::item:hover {
    background-color: #e3f2fd;
}

QFrame#infoFrame {
    border: 1px solid #bdbdbd;
    border-radius: 5px;
    background-color: white;
}

QSplitter::handle {
    background-color: #bdbdbd;
    width: 1px;
}

QScrollBar:vertical {
    border: none;
    background-color: #f5f5f5;
    width: 12px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #bdbdbd;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #9e9e9e;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""