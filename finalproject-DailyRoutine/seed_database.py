import sqlite3
import random
from datetime import date, timedelta

# Import the database manager to ensure tables are created
from database.database import DatabaseManager

# Path to the database file, relative to the project root
DB_PATH = './database/habits.db'

# Pre-defined sample data
HABIT_NAMES = [
    "Membaca Buku", "Olahraga Pagi", "Minum 2L Air", "Belajar Python",
    "Meditasi 10 Menit", "Menulis Jurnal", "Membersihkan Kamar", "Berjalan Kaki 30 Menit",
    "Tidak Makan Gorengan", "Tidur 8 Jam", "Menyiram Tanaman", "Beribadah Tepat Waktu"
]

CATEGORIES = ["Kesehatan", "Belajar", "Produktivitas", "Ibadah", "Hobi", "Pekerjaan Rumah"]
PRIORITIES = ["Tinggi", "Medium", "Rendah"]
STATUSES = ["Belum", "Selesai"]

def seed_database():
    """Clears the existing habits and populates the database with sample data."""
    try:
        # First, ensure the database and tables exist by initializing the manager
        print("Initializing database manager to ensure tables exist...")
        db_manager = DatabaseManager(DB_PATH)
        print("Database tables are ready.")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 1. Clear existing data
        cursor.execute("DELETE FROM habits;")
        print("Cleared existing habits from the database.")

        # 2. Insert new sample data
        for i in range(len(HABIT_NAMES)):
            name = HABIT_NAMES[i]
            category = random.choice(CATEGORIES)
            frequency = random.randint(1, 5)
            start_date = (date.today() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
            status = random.choice(STATUSES)
            priority = random.choice(PRIORITIES)
            target_weekly = frequency
            notes = f"Catatan untuk kebiasaan '{name}'."
            created_at = date.today().strftime("%Y-%m-%d %H:%M:%S")
            updated_at = created_at

            # For demonstration, some habits are completed
            total_completed = 0
            streak_count = 0
            if status == 'Selesai':
                total_completed = random.randint(1, target_weekly)
                streak_count = random.randint(1, 7)

            sql = """
                INSERT INTO habits (name, category, frequency, start_date, status, priority,
                                    target_weekly, notes, created_at, updated_at, total_completed, streak_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
            cursor.execute(sql, (name, category, frequency, start_date, status, priority,
                                 target_weekly, notes, created_at, updated_at, total_completed, streak_count))

        conn.commit()
        print(f"Successfully inserted {len(HABIT_NAMES)} sample habits into the database.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    print("Starting database seeding process...")
    seed_database()
