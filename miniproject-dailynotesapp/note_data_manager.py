import json
from datetime import datetime

class NoteDataManager:
    def __init__(self, file_path='notes_data.json'):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create the JSON file if it doesn't exist."""
        try:
            with open(self.file_path, 'r'):
                pass
        except FileNotFoundError:
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def get_all_notes(self):
        """Load all notes from the JSON file."""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading notes: {str(e)}")
            return []

    def add_note(self, title, category, is_important, content):
        """Add a new note to the JSON file."""
        note = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "title": title,
            "category": category,
            "important": is_important,
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            notes = self.get_all_notes()
            notes.append(note)

            with open(self.file_path, 'w') as f:
                json.dump(notes, f, indent=4)

            return True, note
        except Exception as e:
            return False, str(e)

    def delete_note(self, note_id):
        """Delete a note by its ID."""
        try:
            notes = self.get_all_notes()
            notes = [note for note in notes if note["id"] != note_id]

            with open(self.file_path, 'w') as f:
                json.dump(notes, f, indent=4)

            return True, "Note deleted successfully"
        except Exception as e:
            return False, str(e)

    def update_note(self, note_id, title, category, is_important, content):
        """Update an existing note."""
        try:
            notes = self.get_all_notes()

            for note in notes:
                if note["id"] == note_id:
                    note["title"] = title
                    note["category"] = category
                    note["important"] = is_important
                    note["content"] = content
                    note["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    break

            with open(self.file_path, 'w') as f:
                json.dump(notes, f, indent=4)

            return True, "Note updated successfully"
        except Exception as e:
            return False, str(e)

    def search_notes(self, search_text="", category=None):
        """Search notes by text and/or category."""
        notes = self.get_all_notes()
        filtered_notes = []

        search_text = search_text.lower()

        for note in notes:
            # Skip if category filter is applied and note doesn't match
            if category and category != "All" and note["category"] != category:
                continue

            # Skip if search text is provided and not found in title or content
            if search_text and search_text not in note["title"].lower() and search_text not in note["content"].lower():
                continue

            filtered_notes.append(note)

        return filtered_notes
