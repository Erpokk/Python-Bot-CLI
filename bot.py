from datetime import datetime, timedelta
from collections import defaultdict
import re

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not self.value.isdigit() or len(self.value) != 10:
            raise ValueError("Phone number must consist of 10 digits.")

class Birthday(Field):
    def __init__(self, value):
        super().__init__(datetime.strptime(value, '%d.%m.%Y'))

    @property
    def date(self):
        return self.value.date()

class Address(Field):
    pass

class Email(Field):
    def validate(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise ValueError("Invalid email address.")

    def __init__(self, value):
        super().__init__(value)
        self.validate()

class Record:
    def __init__(self, name, phone=None, birthday=None, address=None, email=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.birthday = Birthday(birthday) if birthday else None
        self.address = Address(address) if address else None
        self.email = Email(email) if email else None
        self.notes = []  # Додавання атрибута для зберігання нотаток

    def add_phone(self, phone):
        if any(phone.value == p.value for p in self.phones):
            raise ValueError("Phone number already exists for this contact")
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return "Phone number updated."
        return "Phone not found."

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    # Методи для роботи з нотатками
    def add_note(self, text):
        self.notes.append(text)

    def edit_note(self, index, new_text):
        try:
            self.notes[index] = new_text
        except IndexError:
            return "Note not found."

    def remove_note(self, index):
        try:
            del self.notes[index]
        except IndexError:
            return "Note not found."

    def list_notes(self):
        return self.notes

    def find_notes(self, text):
        return [note for note in self.notes if text.lower() in note.lower()]

    def get_details(self):
        details = f"Name: {self.name.value}\n"
        details += f"Phone: {', '.join([p.value for p in self.phones]) if self.phones else 'No phone number.'}\n"
        details += f"Address: {self.address.value if self.address else 'No address.'}\n"
        details += f"Email: {self.email.value if self.email else 'No email.'}\n"
        details += f"Birthday: {self.birthday.value.strftime('%d.%m.%Y') if self.birthday else 'Not provided'}\n"
        if self.notes:
            notes_str = "\n".join([f"{idx + 1}: {note}" for idx, note in enumerate(self.notes)])
            details += f"Notes:\n{notes_str}"
        return details

class AddressBook:
    def __init__(self):
        self._records = {}

    def add_record(self, record):
        self._records[record.name.value] = record

    def get_record(self, name):
        return self._records.get(name)

    def get_all_contacts(self):
        return "\n\n".join([record.get_details() for name, record in self._records.items()])

    def get_birthdays_in_next_days(self, days):
        today = datetime.now().date()
        upcoming_birthdays = defaultdict(list)
        for name, record in self._records.items():
            if record.birthday:
                birthday_this_year = record.birthday.date.replace(year=today.year)
                delta = (birthday_this_year - today).days
                if 0 <= delta < days:
                    upcoming_birthdays[birthday_this_year.strftime("%d.%m.%Y")].append(name)
        return "\n".join([f"{date}: {', '.join(names)}" for date, names in upcoming_birthdays.items()])

    def search_contacts(self, search_term):
        results = []
        for name, record in self._records.items():
            if (search_term.lower() in name.lower() or
                any(search_term in phone.value for phone in record.phones) or
                (record.address and search_term.lower() in record.address.value.lower()) or
                (record.email and search_term.lower() in record.email.value.lower())):
                results.append(record.get_details())
        return "\n\n".join(results) if results else "No matching contacts found."

    def edit_record(self, name, phone=None, address=None, email=None, birthday=None):
        if name in self._records:
            record = self._records[name]
            if phone:
                record.phones = [Phone(phone)]
            if address:
                record.address = Address(address)
            if email:
                record.email = Email(email)
            if birthday:
                record.birthday = Birthday(birthday)
            return f"Record for {name} has been updated."
        else:
            return "Record not found."

    def remove_record(self, name):
        if name in self._records:
            del self._records[name]
            return f"Record for {name} has been removed."
        else:
            return "Record not found."

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