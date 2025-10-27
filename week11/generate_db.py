import sqlite3
import random

DATABASE_NAME = 'movies.db'

# Daftar contoh data film (judul, sutradara, tahun, genre)
sample_movies = [
    ("The Shawshank Redemption", "Frank Darabont", 1994, "Drama"),
    ("The Godfather", "Francis Ford Coppola", 1972, "Crime, Drama"),
    ("The Dark Knight", "Christopher Nolan", 2008, "Action, Crime, Drama"),
    ("Pulp Fiction", "Quentin Tarantino", 1994, "Crime, Drama"),
    ("Forrest Gump", "Robert Zemeckis", 1994, "Drama, Romance"),
    ("Inception", "Christopher Nolan", 2010, "Action, Adventure, Sci-Fi"),
    ("The Matrix", "Lana Wachowski, Lilly Wachowski", 1999, "Action, Sci-Fi"),
    ("Interstellar", "Christopher Nolan", 2014, "Adventure, Drama, Sci-Fi"),
    ("Parasite", "Bong Joon Ho", 2019, "Comedy, Drama, Thriller"),
    ("Spirited Away", "Hayao Miyazaki", 2001, "Animation, Adventure, Family"),
    ("Saving Private Ryan", "Steven Spielberg", 1998, "Drama, War"),
    ("The Green Mile", "Frank Darabont", 1999, "Crime, Drama, Fantasy"),
    ("Gladiator", "Ridley Scott", 2000, "Action, Adventure, Drama"),
    ("The Prestige", "Christopher Nolan", 2006, "Drama, Mystery, Sci-Fi"),
    ("Whiplash", "Damien Chazelle", 2014, "Drama, Music"),
    ("The Departed", "Martin Scorsese", 2006, "Crime, Drama, Thriller"),
    ("Avengers: Endgame", "Anthony Russo, Joe Russo", 2019, "Action, Adventure, Drama"),
    ("Joker", "Todd Phillips", 2019, "Crime, Drama, Thriller"),
    ("Your Name.", "Makoto Shinkai", 2016, "Animation, Drama, Fantasy"),
    ("Coco", "Lee Unkrich, Adrian Molina", 2017, "Animation, Adventure, Family"),
    ("Oldboy", "Park Chan-wook", 2003, "Action, Drama, Mystery"),
    ("The Lion King", "Roger Allers, Rob Minkoff", 1994, "Animation, Adventure, Drama"),
    ("Back to the Future", "Robert Zemeckis", 1985, "Adventure, Comedy, Sci-Fi")
]

def create_and_populate_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Membuat tabel jika belum ada (sesuai skema aplikasi Anda)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            director TEXT,
            year INTEGER,
            genre TEXT
        )
    ''')
    conn.commit()

    # Kosongkan tabel dulu jika ingin data selalu fresh dari skrip ini
    # cursor.execute("DELETE FROM movies")
    # conn.commit()

    # Cek apakah tabel sudah ada isinya, jika belum, baru insert
    cursor.execute("SELECT COUNT(*) FROM movies")
    count = cursor.fetchone()[0]

    if count == 0:
        print(f"Memasukkan {len(sample_movies)} data film ke database {DATABASE_NAME}...")
        for movie in sample_movies:
            try:
                title, director, year, genre = movie
                cursor.execute('''
                    INSERT INTO movies (title, director, year, genre)
                    VALUES (?, ?, ?, ?)
                ''', (title, director, year, genre))
            except Exception as e:
                print(f"Error saat memasukkan data '{movie[0]}': {e}")
        conn.commit()
        print("Data berhasil dimasukkan.")
    else:
        print(f"Database {DATABASE_NAME} sudah berisi {count} data. Tidak ada data baru yang dimasukkan oleh skrip ini.")

    conn.close()

if __name__ == '__main__':
    create_and_populate_db()
    print(f"File database '{DATABASE_NAME}' siap digunakan atau sudah ada isinya.")
