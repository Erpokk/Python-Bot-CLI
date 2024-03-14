from datetime import datetime
from objects.Record import Record
from objects.AddressBook import AddressBook
from objects.Notes import Notes


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return inner

@input_error
def add_contact_command(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Not enough arguments. Usage: add [name] [phone] [address (optional)] [email (optional)] [birthday (optional)]")
    name, phone = args[:2]
    address, email, birthday = None, None, None
    if len(args) > 2:
        for arg in args[2:]:
            if '@' in arg:  # Simple check to assume it's an email
                email = arg
            elif '.' in arg and len(arg.split('.')) == 3:  # Simple check to assume it's a date
                try:
                    datetime.strptime(arg, '%d.%m.%Y')  # Validate date format
                    birthday = arg
                except ValueError:
                    print(f"Invalid date format for birthday: {arg}. Expected DD.MM.YYYY.")
            else:
                address = arg  # Assume any other argument is an address
    record = Record(name, phone, birthday, address, email)
    book.add_record(record)
    return "Contact added."

def birthdays_command(args, book: AddressBook):
    if not args or not args[0].isdigit():
        return "Usage: birthdays [number_of_days]"
    days = int(args[0])
    return book.get_birthdays_in_next_days(days)

def search_contacts_command(args, book: AddressBook):
    if len(args) != 1:
        return "Usage: search [search_term]"
    search_term = args[0]
    return book.search_contacts(search_term)

def edit_contact_command(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: edit [name] [phone (optional)] [address (optional)] [email (optional)] [birthday (optional)]"
    name = args[0]
    phone = args[1] if len(args) > 1 else None
    address = args[2] if len(args) > 2 else None
    email = args[3] if len(args) > 3 else None
    birthday = args[4] if len(args) > 4 else None
    return book.edit_record(name, phone, address, email, birthday)

def remove_contact_command(args, book: AddressBook):
    if len(args) != 1:
        return "Usage: remove [name]"
    name = args[0]
    return book.remove_record(name)

def hello_command(args):
    return "Hello! How can I assist you today?"

def show_all_contacts_command(args, book: AddressBook):
    return book.get_all_contacts()


def add_comment_command(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: add_note [name] [comment_text]"
    name, note_text = args[0], " ".join(args[1:])
    return book.add_comment(name, note_text)
  

def remove_comment_command(args, book: AddressBook):
    if len(args) != 1:
        return "Usage: remove-note [name]"
    name = args[0]
    return book.remove_comment(name)
    

def add_notes_command(args, notes_dif: Notes):
    note_text = " ".join(args)
    notes_dif.add_notes(note_text)
    return "Note added."

def edit_notes_command(args, notes_dif: Notes):
    if len(args) < 2:
        return "Usage: edit-notes [note_id] [new_note]"

    try:
        note_id = int(args[0]) - 1  # Перетворення в індекс Python
        new_note = " ".join(args[1:])
        return notes_dif.edit_notes(note_id, new_note)
    except ValueError:
        return "Invalid note ID."
    
def remove_notes_command(args, notes_dif: Notes):
    try:
        note_id = int(args[0]) - 1  # Перетворення в індекс Python
        return notes_dif.remove_notes(note_id)
    except ValueError:
        return "Invalid note ID."

def list_notes_command(args, notes_dif: Notes):
    return notes_dif.list_notes_command()

def find_notes_command(args, notes_dif: Notes):
    search_text = " ".join(args)
    return notes_dif.find_notes_command(search_text)
    