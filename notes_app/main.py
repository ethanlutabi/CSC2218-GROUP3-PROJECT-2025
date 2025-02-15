import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label

class NotesDB:
    def __init__(self):
        self.conn = sqlite3.connect("notes.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id  INTEGER PRIMAY KEY,
        content TEXT
        )
""")
        self.conn.commit()
        
    def add_note(self,content):
        self.cursor.execute("INSERT INTO notes (content) VALUES (?)",(content,))
        self.conn.commit()

    def get_notes(self):
        self.cursor.execute("SELECT content FROM notes")
        notes = [row[0] for row in self.cursor.fetchall()]
        print("Loaded Notes:", notes)  # Debugging line
        return notes



class NotesApp(App):
    def build(self):
        self.notes = []
        self.layout = BoxLayout(orientation="vertical")

        self.note_input = TextInput(hint_text= "Enter your text here")
        self.save_button = Button(text= "Save note")
        self.save_button.bind(on_press = self.save_note)

        self.notes_label = Label(text= "No notes yet")


        self.layout.add_widget(self.note_input)
        self.layout.add_widget(self.save_button)
        self.layout.add_widget(self.notes_label)
        return self.layout
    

    def save_note(self, instance):
        note = self.note_input.text.strip()
        if note:
            self.notes.append(note)
            self.notes_label.text = "\n".join(self.notes)
            self.note_input.text = ""

NotesApp().run()  # Run the app
