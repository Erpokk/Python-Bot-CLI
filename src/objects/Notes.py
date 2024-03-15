from servises.SaveService import SaveService

class Notes:
    """
    Represents a collection of notes.

    Attributes:
        name_for_save (str): A string representing the name used for saving notes.
        
    Methods:
        __init__: Initializes a Notes instance with a save service.
        add_notes: Adds a new note to the collection.
        edit_notes: Edits an existing note in the collection.
        remove_notes: Removes a note from the collection.
        list_notes_command: Lists all notes in the collection.
        find_notes_command: Finds notes containing a specific text.
    """
    name_for_save = "notes"
    
    def __init__(self, save_service: SaveService):
        """
        Initializes a Notes instance.

        Args:
            save_service (SaveService): An instance of the SaveService class for saving notes data.
        """
        self._save_service = save_service
        
        loaded_data = save_service.load(Notes.name_for_save)
        if loaded_data == None:
            self.notes = []
        else:
            self.notes = loaded_data

    def add_notes(self, note):
        """
        Adds a new note to the collection.

        Args:
            note (str): The note to add.
        """
        self.notes.append(note)
        self._save_service.save(Notes.name_for_save, self.notes)

    def edit_notes(self, note_id, new_note):
        """
        Edits an existing note in the collection.

        Args:
            note_id (int): The ID of the note to edit.
            new_note (str): The new content of the note.
        
        Returns:
            str: A message indicating whether the note was successfully updated or not.
        """
        if 0 <= note_id < len(self.notes):
            self.notes[note_id] = new_note
            self._save_service.save(Notes.name_for_save, self.notes)
            return "Note updated."
        else:
            return "Note not found."

    def remove_notes(self, note_id):
        """
        Removes a note from the collection.

        Args:
            note_id (int): The ID of the note to remove.
        
        Returns:
            str: A message indicating whether the note was successfully removed or not.
        """
        if 0 <= note_id < len(self.notes):
            del self.notes[note_id]
            self._save_service.save(Notes.name_for_save, self.notes)
            return "Note removed."
        else:
            return "Note not found."

    def list_notes_command(self):
        """
        Lists all notes in the collection.

        Returns:
            str: A string containing all notes in the collection.
        """
        if self.notes:
            return "\n".join([f"{idx + 1}: {note}" for idx, note in enumerate(self.notes)])
        else:
            return "No notes available."

    def find_notes_command(self, search_text):
        """
        Finds notes containing a specific text.

        Args:
            search_text (str): The text to search for in the notes.

        Returns:
            str: A string containing the matching notes, if any.
        """
        found_notes = [note for note in self.notes if search_text.lower() in note.lower()]
        if found_notes:
            return "\n".join(found_notes)
        else:
            return "No matching notes found."
