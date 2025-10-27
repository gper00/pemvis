"""
Helper functions for DailyRoutine application
"""

import os
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path

from config.constants import (
    HABIT_CATEGORIES, HABIT_PRIORITIES, HABIT_STATUS,
    PRIORITY_COLORS, STATUS_COLORS, DATE_FORMAT, DISPLAY_DATE_FORMAT
)

def format_date_for_display(date_str: str) -> str:
    """Format date string for display"""
    try:
        if isinstance(date_str, str):
            parsed_date = datetime.fromisoformat(date_str).date()
            return parsed_date.strftime(DISPLAY_DATE_FORMAT)
        return str(date_str)
    except (ValueError, AttributeError):
        return date_str

def format_date_for_database(date_obj: date) -> str:
    """Format date object for database storage"""
    return date_obj.isoformat()

def get_priority_color(priority: str) -> str:
    """Get color for priority level"""
    return PRIORITY_COLORS.get(priority, "#7f8c8d")

def get_status_color(status: str) -> str:
    """Get color for status"""
    return STATUS_COLORS.get(status, "#7f8c8d")

def calculate_completion_rate(completed: int, total: int) -> float:
    """Calculate completion rate percentage"""
    if total == 0:
        return 0.0
    return (completed / total) * 100

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to specified length"""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def ensure_directory(path: str) -> None:
    """Ensure directory exists"""
    Path(path).mkdir(parents=True, exist_ok=True)

def get_file_size_mb(file_path: str) -> float:
    """Get file size in megabytes"""
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except OSError:
        return 0.0

def format_file_size(size_mb: float) -> str:
    """Format file size for display"""
    if size_mb < 1:
        return f"{size_mb * 1024:.1f} KB"
    return f"{size_mb:.1f} MB"

def validate_file_path(file_path: str) -> bool:
    """Validate file path"""
    try:
        Path(file_path)
        return True
    except Exception:
        return False

def get_habit_summary(habits: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Get summary statistics for habits"""
    total = len(habits)
    completed = sum(1 for habit in habits if habit.get('status') == 'Selesai')
    pending = total - completed

    # Category breakdown
    category_count = {}
    for habit in habits:
        category = habit.get('category', 'Unknown')
        category_count[category] = category_count.get(category, 0) + 1

    # Priority breakdown
    priority_count = {'High': 0, 'Medium': 0, 'Low': 0}
    for habit in habits:
        priority = habit.get('priority', 'Medium')
        if priority in priority_count:
            priority_count[priority] += 1

    return {
        'total': total,
        'completed': completed,
        'pending': pending,
        'completion_rate': calculate_completion_rate(completed, total),
        'category_breakdown': category_count,
        'priority_breakdown': priority_count
    }

def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, AttributeError):
        return timestamp

def get_current_week_dates() -> List[str]:
    """Get list of dates for current week"""
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    week_dates = []

    for i in range(7):
        week_date = start_of_week + timedelta(days=i)
        week_dates.append(week_date.isoformat())

    return week_dates

def is_today(date_str: str) -> bool:
    """Check if date string is today"""
    try:
        check_date = datetime.fromisoformat(date_str).date()
        return check_date == date.today()
    except (ValueError, AttributeError):
        return False

def get_weekday_name(date_str: str) -> str:
    """Get weekday name from date string"""
    try:
        check_date = datetime.fromisoformat(date_str).date()
        return check_date.strftime("%A")
    except (ValueError, AttributeError):
        return "Unknown"

def create_backup_filename(prefix: str = "backup") -> str:
    """Create backup filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.db"

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')

    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext

    return filename

def get_application_info() -> Dict[str, str]:
    """Get application information"""
    from config.constants import APP_NAME, APP_VERSION, AUTHOR, NIM

    return {
        'name': APP_NAME,
        'version': APP_VERSION,
        'author': AUTHOR,
        'nim': NIM,
        'build_date': datetime.now().strftime("%Y-%m-%d")
    }
