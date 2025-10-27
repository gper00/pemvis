"""
Database operations for DailyRoutine application
"""

import sqlite3
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

from config.constants import DATABASE_PATH, HABIT_CATEGORIES, HABIT_PRIORITIES, HABIT_STATUS

class DatabaseManager:
    """SQLite database manager for habits"""

    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self._ensure_database_directory()
        self._create_tables()

    def _ensure_database_directory(self) -> None:
        """Ensure database directory exists"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def _create_tables(self) -> None:
        """Create database tables if they don't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Create habits table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        category TEXT NOT NULL,
                        start_date TEXT NOT NULL,
                        frequency INTEGER NOT NULL CHECK (frequency >= 1 AND frequency <= 7),
                        status TEXT NOT NULL DEFAULT 'Belum',
                        notes TEXT,
                        priority TEXT NOT NULL DEFAULT 'Medium',
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        target_weekly INTEGER NOT NULL DEFAULT 1,
                        streak_count INTEGER NOT NULL DEFAULT 0,
                        total_completed INTEGER NOT NULL DEFAULT 0
                    )
                """)

                # Create habit_logs table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS habit_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        habit_id INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        completed BOOLEAN NOT NULL DEFAULT 0,
                        notes TEXT,
                        created_at TEXT NOT NULL,
                        FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
                    )
                """)

                # Create categories table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        color TEXT NOT NULL,
                        icon TEXT
                    )
                """)

                # Create indexes for better performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_habits_category ON habits(category)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_habits_status ON habits(status)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_habits_priority ON habits(priority)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_habits_created_at ON habits(created_at)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_habit_logs_habit_id ON habit_logs(habit_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_habit_logs_date ON habit_logs(date)")

                # Insert default categories if they don't exist
                self._insert_default_categories(cursor)

                conn.commit()
                print("Database tables created successfully")

        except sqlite3.Error as e:
            print(f"Error creating database tables: {e}")
            raise

    def _insert_default_categories(self, cursor: sqlite3.Cursor) -> None:
        """Insert default categories"""
        default_categories = [
            ("Umum", "#3498db", "general"),
            ("Kesehatan", "#e74c3c", "health"),
            ("Belajar", "#9b59b6", "study"),
            ("Ibadah", "#f39c12", "prayer"),
            ("Olahraga", "#27ae60", "sport"),
            ("Kerja", "#34495e", "work"),
            ("Sosial", "#e67e22", "social"),
            ("Hobi", "#1abc9c", "hobby")
        ]

        for name, color, icon in default_categories:
            cursor.execute("""
                INSERT OR IGNORE INTO categories (name, color, icon)
                VALUES (?, ?, ?)
            """, (name, color, icon))

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()

    def create_habit(self, habit_data: Dict[str, Any]) -> int:
        """Create a new habit"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                current_time = self._get_current_timestamp()

                cursor.execute("""
                    INSERT INTO habits (
                        name, category, start_date, frequency, status, notes,
                        priority, created_at, updated_at, target_weekly
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    habit_data['name'],
                    habit_data['category'],
                    habit_data['start_date'],
                    habit_data['frequency'],
                    habit_data.get('status', 'Belum'),
                    habit_data.get('notes', ''),
                    habit_data.get('priority', 'Medium'),
                    current_time,
                    current_time,
                    habit_data.get('target_weekly', 1)
                ))

                habit_id = cursor.lastrowid
                conn.commit()
                print(f"Habit created with ID: {habit_id}")
                return habit_id

        except sqlite3.IntegrityError as e:
            print(f"Integrity error creating habit: {e}")
            raise ValueError("Habit name already exists")
        except sqlite3.Error as e:
            print(f"Error creating habit: {e}")
            raise

    def update_habit(self, habit_id: int, habit_data: Dict[str, Any]) -> bool:
        """Update an existing habit"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                current_time = self._get_current_timestamp()

                cursor.execute("""
                    UPDATE habits SET
                        name = ?, category = ?, start_date = ?, frequency = ?,
                        status = ?, notes = ?, priority = ?, updated_at = ?,
                        target_weekly = ?
                    WHERE id = ?
                """, (
                    habit_data['name'],
                    habit_data['category'],
                    habit_data['start_date'],
                    habit_data['frequency'],
                    habit_data.get('status', 'Belum'),
                    habit_data.get('notes', ''),
                    habit_data.get('priority', 'Medium'),
                    current_time,
                    habit_data.get('target_weekly', 1),
                    habit_id
                ))

                if cursor.rowcount == 0:
                    print(f"Warning: Habit with ID {habit_id} not found for update")
                    return False

                conn.commit()
                print(f"Habit {habit_id} updated successfully")
                return True

        except sqlite3.IntegrityError as e:
            print(f"Integrity error updating habit: {e}")
            raise ValueError("Habit name already exists")
        except sqlite3.Error as e:
            print(f"Error updating habit: {e}")
            raise

    def delete_habit(self, habit_id: int) -> bool:
        """Delete a habit"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))

                if cursor.rowcount == 0:
                    print(f"Warning: Habit with ID {habit_id} not found for deletion")
                    return False

                conn.commit()
                print(f"Habit {habit_id} deleted successfully")
                return True

        except sqlite3.Error as e:
            print(f"Error deleting habit: {e}")
            raise

    def get_habit(self, habit_id: int) -> Optional[Dict[str, Any]]:
        """Get a habit by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
                row = cursor.fetchone()

                if row:
                    return dict(row)
                return None

        except sqlite3.Error as e:
            print(f"Error getting habit: {e}")
            raise

    def get_all_habits(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all habits with optional filters"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                query = "SELECT * FROM habits WHERE 1=1"
                params = []

                if filters:
                    if filters.get('category'):
                        query += " AND category = ?"
                        params.append(filters['category'])

                    if filters.get('status'):
                        query += " AND status = ?"
                        params.append(filters['status'])

                    if filters.get('priority'):
                        query += " AND priority = ?"
                        params.append(filters['priority'])

                    if filters.get('search'):
                        query += " AND (name LIKE ? OR notes LIKE ?)"
                        search_term = f"%{filters['search']}%"
                        params.extend([search_term, search_term])

                query += " ORDER BY created_at DESC"

                cursor.execute(query, params)
                rows = cursor.fetchall()

                return [dict(row) for row in rows]

        except sqlite3.Error as e:
            print(f"Error getting habits: {e}")
            raise

    def mark_habit_complete(self, habit_id: int, completion_date: str = None) -> bool:
        """Mark a habit as completed for a specific date"""
        try:
            if completion_date is None:
                completion_date = date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Check if log already exists for this date
                cursor.execute("""
                    SELECT id FROM habit_logs
                    WHERE habit_id = ? AND date = ?
                """, (habit_id, completion_date))

                existing_log = cursor.fetchone()

                if existing_log:
                    # Update existing log
                    cursor.execute("""
                        UPDATE habit_logs SET completed = 1, updated_at = ?
                        WHERE habit_id = ? AND date = ?
                    """, (self._get_current_timestamp(), habit_id, completion_date))
                else:
                    # Create new log
                    cursor.execute("""
                        INSERT INTO habit_logs (habit_id, date, completed, created_at)
                        VALUES (?, ?, 1, ?)
                    """, (habit_id, completion_date, self._get_current_timestamp()))

                # Update habit statistics
                self._update_habit_statistics(cursor, habit_id)

                conn.commit()
                print(f"Habit {habit_id} marked complete for {completion_date}")
                return True

        except sqlite3.Error as e:
            print(f"Error marking habit complete: {e}")
            raise

    def _update_habit_statistics(self, cursor: sqlite3.Cursor, habit_id: int) -> None:
        """Update habit statistics (streak, total completed)"""
        # Calculate total completed
        cursor.execute("""
            SELECT COUNT(*) FROM habit_logs
            WHERE habit_id = ? AND completed = 1
        """, (habit_id,))
        total_completed = cursor.fetchone()[0]

        # Calculate current streak (simplified)
        cursor.execute("""
            SELECT COUNT(*) FROM habit_logs
            WHERE habit_id = ? AND completed = 1
            ORDER BY date DESC
        """, (habit_id,))
        streak_count = cursor.fetchone()[0]

        # Update habit
        cursor.execute("""
            UPDATE habits SET
                total_completed = ?, streak_count = ?, updated_at = ?
            WHERE id = ?
        """, (total_completed, streak_count, self._get_current_timestamp(), habit_id))

    def get_statistics(self) -> Dict[str, Any]:
        """Get application statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Total habits
                cursor.execute("SELECT COUNT(*) FROM habits")
                total_habits = cursor.fetchone()[0]

                # Completed habits
                cursor.execute("SELECT COUNT(*) FROM habits WHERE status = 'Selesai'")
                completed_habits = cursor.fetchone()[0]

                # Pending habits
                cursor.execute("SELECT COUNT(*) FROM habits WHERE status = 'Belum'")
                pending_habits = cursor.fetchone()[0]

                # Category breakdown
                cursor.execute("""
                    SELECT category, COUNT(*) as count
                    FROM habits
                    GROUP BY category
                """)
                category_breakdown = dict(cursor.fetchall())

                # Priority breakdown
                cursor.execute("""
                    SELECT priority, COUNT(*) as count
                    FROM habits
                    GROUP BY priority
                """)
                priority_breakdown = dict(cursor.fetchall())

                return {
                    'total_habits': total_habits,
                    'completed_habits': completed_habits,
                    'pending_habits': pending_habits,
                    'completion_rate': (completed_habits / total_habits * 100) if total_habits > 0 else 0,
                    'category_breakdown': category_breakdown,
                    'priority_breakdown': priority_breakdown
                }

        except sqlite3.Error as e:
            print(f"Error getting statistics: {e}")
            raise

    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all categories"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM categories ORDER BY name")
                rows = cursor.fetchall()

                return [dict(row) for row in rows]

        except sqlite3.Error as e:
            print(f"Error getting categories: {e}")
            raise

# Global database instance
db_manager = DatabaseManager()
