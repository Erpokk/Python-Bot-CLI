
import re
#import json
import os

# РОМА, нижче подаю блоки коду, де я вносив доповнення і зміни для введення функціоналу кількох номерів телефону в один контакт;
# для виконання задачі пошуку в нотатках, довелося фактчно закодити весь клас, який я трішки переназвав - "NotesDif" (Different) 
# та додав нові команди іфункціонал для цього класу


class NotesDif:
    def __init__(self, save_service: SaveService):
        self.notes = save_service.load('notes') if save_service.load('notes') else []
        self._save_service = save_service

    def add_notes(self, note):
        self.notes.append(note)
        self._save_service.save('notes', self.notes)

    def edit_notes(self, note_id, new_note):
        if 0 <= note_id < len(self.notes):
            self.notes[note_id] = new_note
            self._save_service.save('notes', self.notes)
            return "Note updated."
        else:
            return "Note not found."

    def remove_notes(self, note_id):
        if 0 <= note_id < len(self.notes):
            del self.notes[note_id]
            self._save_service.save('notes', self.notes)
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
        


class Phone(Field):

    def __init__(self, value):
        super().__init__(value)
        self.validate(value)

    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must consist of 10 digits.")


    def add_phone(self, phone):
        if phone not in self.values:
            self.values.append(phone)

    def remove_phone(self, phone):
        if phone in self.values:
            self.values.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.values:
            self.values[self.values.index(old_phone)] = new_phone


class Record:   # добавлено 'phones'
    def __init__(self, name, phones=None, birthday=None, address=None, email=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones] if phones else []
        self.birthday = Birthday(birthday) if birthday else None
        self.address = Address(address) if address else None
        self.email = Email(email) if email else None
        self.notes = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))    


# відредактований код для функціоналу введення декількох номерів тел.
@input_error
def add_contact_command(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Not enough arguments. Usage: add [name] [phone,phone2,...] [address (optional)] [email (optional)] [birthday (optional)]")
    name = args[0]
    # Розділення другого аргументу за комами для отримання списку номерів телефонів
    phones = args[1].split(',')
    address, email, birthday = None, None, None
    if len(args) > 2:
        for arg in args[2:]:
            if '@' in arg:
                email = arg
            elif '.' in arg and len(arg.split('.')) == 3:
                try:
                    datetime.strptime(arg, '%d.%m.%Y')
                    birthday = arg
                except ValueError:
                    print(f"Invalid date format for birthday: {arg}. Expected DD.MM.YYYY.")
            else:
                address = arg
    record = Record(name, phones, birthday, address, email)
    book.add_record(record)
    return "Contact added."

def edit_contact_command(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: edit [name] [phone (optional)] [address (optional)] [email (optional)] [birthday (optional)]"
    name = args[0]
    phone = args[1] if len(args) > 1 else None
    address = args[2] if len(args) > 2 else None
    email = args[3] if len(args) > 3 else None
    birthday = args[4] if len(args) > 4 else None
    return book.edit_record(name, phone, address, email, birthday)


# функціонал нових команд для Нотаток (class NotesDif)
def add_notes_command(args, notes_dif: NotesDif):
    note_text = " ".join(args)
    notes_dif.add_notes(note_text)
    return "Note added."

def edit_notes_command(args, notes_dif: NotesDif):
    if len(args) < 2:
        return "Usage: edit-notes [note_id] [new_note]"

    try:
        note_id = int(args[0]) - 1  # Перетворення в індекс Python
        new_note = " ".join(args[1:])
        return notes_dif.edit_notes(note_id, new_note)
    except ValueError:
        return "Invalid note ID."

def remove_notes_command(args, notes_dif: NotesDif):
    try:
        note_id = int(args[0]) - 1  # Перетворення в індекс Python
        return notes_dif.remove_notes(note_id)
    except ValueError:
        return "Invalid note ID."

def list_notes_command(args, notes_dif: NotesDif):
    return notes_dif.list_notes_command()

def find_notes_command(args, notes_dif: NotesDif):
    search_text = " ".join(args)
    return notes_dif.find_notes_command(search_text)

# додано команди для роботи з нотатками (class NotesDif). add- додає нт., remove- видаляє нт, edit- редактує нт, list- виводить всі нт,\
# find- здійснює пошук введеного слова(цифри) в нт-ках


def main():
    save_service = SaveService()
    book = AddressBook(save_service)
    notes_dif = NotesDif(save_service)

    commands = {
        
        "add-notes": lambda args: add_notes_command(args, notes_dif),
        "remove-notes": lambda args: remove_notes_command(args, notes_dif),
        "edit-notes": lambda args: edit_notes_command(args, notes_dif),
        "list-notes": lambda args: list_notes_command(args, notes_dif),
        "find-notes": lambda args: find_notes_command(args, notes_dif),
        #"save-info": lambda _: "All information has been saved automatically." - це планував команду для збереження інформації...
    }

# ці зміни необхідні були для роботи функції введення декількох телефонів
print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").lower().split()
        if not user_input:                                       # Перевіряємо, чи список не порожній
            print("No command entered. Please try again.")
            continue 

        command, args = user_input[0], user_input[1:]



# на сам кінець - сирий код для функціоналу "зберігання",який я не зміг доробити, можливо буде корисним...
class SaveService:
    def __init__(self):
        self.storage = {}

    def save(self, key, data):
        self.storage[key] = data

    def load(self, key):
        return self.storage.get(key, None)

#     def __init__(self, filename='data.json'):
#         self.filename = filename
#         self.storage = self.load_from_file()

#     def save(self, key, data):
#         self.storage[key] = data
#         self.save_to_file()

#     def load(self, key):
#         return self.storage.get(key, None)

#     def save_to_file(self):
#         with open(self.filename, 'w') as f:
#             json.dump(self.storage, f)

#     def load_from_file(self):
#         if os.path.exists(self.filename):
#             with open(self.filename, 'r') as f:
#                 return json.load(f)
#         return {}