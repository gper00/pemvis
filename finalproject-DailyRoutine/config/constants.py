"""
Constants for DailyRoutine application
"""

# Application Information
APP_NAME = "DailyRoutine"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Habit Tracker Application"
AUTHOR = "UMAM ALPARIZI"
NIM = "F1D02310141"

# Database Configuration
DATABASE_NAME = "habits.db"
DATABASE_PATH = "database/habits.db"

# UI Configuration
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Habit Categories
HABIT_CATEGORIES = [
    "Umum",
    "Kesehatan",
    "Belajar",
    "Ibadah",
    "Olahraga",
    "Kerja",
    "Sosial",
    "Hobi"
]

# Habit Priorities
HABIT_PRIORITIES = ["Low", "Medium", "High"]

# Habit Status
HABIT_STATUS = ["Belum", "Selesai"]

# Export Configuration
EXPORT_DIR = "exports"
CSV_EXTENSION = ".csv"
PDF_EXTENSION = ".pdf"

# Styling Colors
COLORS = {
    "primary": "#3498db",
    "secondary": "#2c3e50",
    "success": "#27ae60",
    "warning": "#f39c12",
    "danger": "#e74c3c",
    "light_bg": "#f5f5f5",
    "dark_bg": "#2c3e50",
    "text_primary": "#2c3e50",
    "text_secondary": "#7f8c8d",
    "border": "#bdc3c7"
}

# Priority Colors
PRIORITY_COLORS = {
    "Low": "#27ae60",
    "Medium": "#f39c12",
    "High": "#e74c3c"
}

# Status Colors
STATUS_COLORS = {
    "Selesai": "#27ae60",
    "Belum": "#f39c12"
}

# File Paths
ASSETS_DIR = "assets"
ICONS_DIR = "assets/icons"
STYLES_DIR = "assets/styles"
IMAGES_DIR = "assets/images"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "dailyroutine.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Validation Rules
MAX_HABIT_NAME_LENGTH = 100
MAX_NOTES_LENGTH = 500
MIN_FREQUENCY = 1
MAX_FREQUENCY = 7

# Date Formats
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DISPLAY_DATE_FORMAT = "%d/%m/%Y"

# Keyboard Shortcuts
SHORTCUTS = {
    "new_habit": "Ctrl+N",
    "save": "Ctrl+S",
    "exit": "Ctrl+Q",
    "export_pdf": "Ctrl+P",
    "export_csv": "Ctrl+E",
    "help": "F1"
}
