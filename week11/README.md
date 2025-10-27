# Movie Collection Manager

A simple desktop application built with PyQt5 to manage your movie collection.

## Requirements

- Python 3.x
- PyQt5
- SQLite3

## Installation

1. Make sure Python 3.x is installed on your system
2. Install required package:
   ```
   pip install PyQt5
   ```
3. Run the application:
   ```
   python app.py
   ```

## Sample Data

To populate the database with sample movie data, you can run:
```
python generate_db.py
```
This will create a database with 23 sample movies if the database is empty. If the database already contains data, the script will not add duplicate entries.

## Features

- Add, edit, and delete movies from your collection
- Search movies by title, director, or genre
- Export your collection to CSV
- Paste movie titles directly from clipboard
- Help panel with usage instructions
- Clean modern interface

## Usage

1. Launch the app by running `app.py`
2. Add movies using the input form at the top
3. Double-click any entry in the table to edit it
4. Use the search panel to filter your collection
5. Export your data using the CSV export button
6. To start with sample data, run `generate_db.py` before running the app

## Database

The application uses SQLite database (`movies.db`) to store your movie collection. The database file will be created automatically when you first run the application.
