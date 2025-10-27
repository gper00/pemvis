"""
Custom exceptions for DailyRoutine application
"""

class DailyRoutineError(Exception):
    """Base exception for DailyRoutine application"""
    pass

class DatabaseError(DailyRoutineError):
    """Exception raised for database-related errors"""
    pass

class ValidationError(DailyRoutineError):
    """Exception raised for validation errors"""
    pass

class ExportError(DailyRoutineError):
    """Exception raised for export-related errors"""
    pass

class UIError(DailyRoutineError):
    """Exception raised for UI-related errors"""
    pass

class ConfigError(DailyRoutineError):
    """Exception raised for configuration errors"""
    pass

class HabitNotFoundError(DailyRoutineError):
    """Exception raised when habit is not found"""
    pass

class DuplicateHabitError(DailyRoutineError):
    """Exception raised when habit name already exists"""
    pass

class InvalidDateFormatError(DailyRoutineError):
    """Exception raised for invalid date format"""
    pass

class FileOperationError(DailyRoutineError):
    """Exception raised for file operation errors"""
    pass
