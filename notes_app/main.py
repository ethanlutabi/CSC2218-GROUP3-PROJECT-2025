import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label


class NotesDB:
    def __init__(self):
        self.conn = sqlite3.connect("notes.db")
        self.cursor = self.conn.cursor()

        # Create the table with the correct schema
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_note(self, content):
        # Insert a note into the database
        self.cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
        self.conn.commit()

    def get_notes(self):
        # Retrieve all notes from the database
        self.cursor.execute("SELECT content FROM notes")
        notes = [row[0] for row in self.cursor.fetchall()]
        return notes


class NotesApp(App):
    def build(self):
        # Initialize the database class each time the app starts
        self.db = NotesDB()

        # Load the notes from the database when the app starts
        self.notes = self.db.get_notes()

        # Set up the UI
        self.layout = BoxLayout(orientation="vertical")

        self.note_input = TextInput(hint_text="Enter your text here")
        self.save_button = Button(text="Save note")
        self.save_button.bind(on_press=self.save_note)

        self.notes_label = Label(text="No notes yet" if not self.notes else "\n".join(self.notes))

        self.layout.add_widget(self.note_input)
        self.layout.add_widget(self.save_button)
        self.layout.add_widget(self.notes_label)

        return self.layout

    def save_note(self, instance):
        note = self.note_input.text.strip()
        if note:
            # Save the note to the database
            self.db.add_note(note)

            # Update the displayed notes
            self.notes = self.db.get_notes()
            self.notes_label.text = "\n".join(self.notes)

            # Clear the input field
            self.note_input.text = ""


if __name__ == "__main__":
    NotesApp().run()
