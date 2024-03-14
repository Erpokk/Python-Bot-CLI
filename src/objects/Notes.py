from servises.SaveService import SaveService

class Notes:
    
    name_for_save = "notes"
    
    def __init__(self, save_service: SaveService):
        self._save_service = save_service
        
        loaded_data = save_service.load(Notes.name_for_save)
        if loaded_data == None:
            self.notes = []
        else:
            self.notes = loaded_data

    def add_notes(self, note):
        self.notes.append(note)
        self._save_service.save(Notes.name_for_save, self.notes)

    def edit_notes(self, note_id, new_note):
        if 0 <= note_id < len(self.notes):
            self.notes[note_id] = new_note
            self._save_service.save(Notes.name_for_save, self.notes)
            return "Note updated."
        else:
            return "Note not found."

    def remove_notes(self, note_id):
        if 0 <= note_id < len(self.notes):
            del self.notes[note_id]
            self._save_service.save(Notes.name_for_save, self.notes)
            return "Note removed."
        else:
            return "Note not found."

    def list_notes_command(self):
        if self.notes:
            return "\n".join([f"{idx + 1}: {note}" for idx, note in enumerate(self.notes)])
        else:
            return "No notes available."

    def find_notes_command(self, search_text):
        found_notes = [note for note in self.notes if search_text.lower() in note.lower()]
        if found_notes:
            return "\n".join(found_notes)
        else:
            return "No matching notes found."
