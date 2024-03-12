from classes import AddressBook, Record, Field, Phone, Birthday, Name
from datetime import datetime

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

# Функції для обробки команд нотаток
def add_note_command(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: add_note [name] [note_text]"
    name, note_text = args[0], " ".join(args[1:])
    record = book.get_record(name)
    if record:
        record.add_note(note_text)
        return "Note added."
    else:
        return "Record not found."

def remove_note_command(args, book: AddressBook):
    if len(args) != 2 or not args[1].isdigit():
        return "Usage: remove-note [name] [note_index]"
    name, note_index = args[0], int(args[1]) - 1  # Зверніть увагу на віднімання 1, щоб врахувати індексацію з нуля
    record = book.get_record(name)
    if record:
        result = record.remove_note(note_index)
        return result if result else "Note removed."
    else:
        return "Record not found."

def edit_note_command(args, book: AddressBook):
    if len(args) < 3 or not args[1].isdigit():
        return "Usage: edit_note [name] [note_index] [new_text]"
    name, note_index, new_text = args[0], int(args[1]) - 1, " ".join(args[2:])
    record = book.get_record(name)
    if record:
        result = record.edit_note(note_index, new_text)
        return result if result else "Note updated."
    else:
        return "Record not found."

def list_notes_command(args, book: AddressBook):
    if len(args) < 1:
        return "Usage: list_notes [name]"
    name = args[0]
    record = book.get_record(name)
    if record:
        notes = record.list_notes()
        if notes:
            return "\n".join([f"{idx + 1}: {note}" for idx, note in enumerate(notes)])
        else:
            return "No notes for this record."
    else:
        return "Record not found."

def find_notes_command(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: find_notes [name] [search_text]"
    name, search_text = args[0], " ".join(args[1:])
    record = book.get_record(name)
    if record:
        found_notes = record.find_notes(search_text)
        if found_notes:
            return "\n".join([f"{idx + 1}: {note}" for idx, note in enumerate(found_notes)])
        else:
            return "No matching notes found."
    else:
        return "Record not found."
    
    
def main():
    book = AddressBook()
    commands = {
        "add": lambda args: add_contact_command(args, book),
        "edit": lambda args: edit_contact_command(args, book),
        "remove": lambda args: remove_contact_command(args, book),       
        "birthdays": lambda args: birthdays_command(args, book),        
        "hello": lambda args: hello_command(args),
        "all": lambda args: show_all_contacts_command(args, book),
        "search": lambda args: search_contacts_command(args, book),
        "add-note": lambda args: add_note_command(args, book),
        "remove-note": lambda args: remove_note_command(args, book),
        "edit-note": lambda args: edit_note_command(args, book),
        "list-notes": lambda args: list_notes_command(args, book),
        "find-notes": lambda args: find_notes_command(args, book),
    }

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").lower().split()
        command, args = user_input[0], user_input[1:]

        if command in ["exit", "close"]:
            print("Good bye!")
            break

        handler = commands.get(command)
        if not handler:
            print("Invalid command.")
            continue

        result = handler(args)
        if result:
            print(result)

if __name__ == "__main__":
    main()