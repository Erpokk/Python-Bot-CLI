from datetime import datetime, timedelta
from collections import defaultdict
import re
#import json
import os


class Field:
    def __init__(self, value):
        self.value = value

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


class AddressBook:
    def __init__(self, save_service: SaveService):
        self._records = save_service.load('contacts') if save_service.load('contacts') else {}
        self._save_service = save_service

    def add_record(self, record):
        self._records[record.name.value] = record
        self._save_service.save('contacts', self._records)

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

class Birthday(Field):
    def __init__(self, value):
        super().__init__(datetime.strptime(value, '%d.%m.%Y'))

    @property
    def date(self):
        return self.value.date()

class Email(Field):

    def validate(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise ValueError("Invalid email address.")

    def __init__(self, value):
        super().__init__(value)
        self.validate()

class Address(Field):
    pass

class Name(Field):
    pass

class Notes:
    def __init__(self, save_service: SaveService):
        self.notes = save_service.load('notes') if save_service.load('notes') else []
        self._save_service = save_service

    def add_note(self, note):
        self.notes.append(note)
        self._save_service.save('notes', self.notes)

    def edit_note(self, note_id, new_note):
        if 0 <= note_id < len(self.notes):
            self.notes[note_id] = new_note
            self._save_service.save('notes', self.notes)
            return "Note updated."
        else:
            return "Note not found."

    def remove_note(self, note_id):
        if 0 <= note_id < len(self.notes):
            del self.notes[note_id]
            self._save_service.save('note', self.notes)
            return "Note removed."
        else:
            return "Note not found."

    def list_note_command(self):
        if self.notes:
            return "\n".join([f"{idx + 1}: {note}" for idx, note in enumerate(self.notes)])
        else:
            return "No notes available."

    def find_note_command(self, search_text):
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

class Record:
    def __init__(self, name, phones=None, birthday=None, address=None, email=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones] if phones else []
        self.birthday = Birthday(birthday) if birthday else None
        self.address = Address(address) if address else None
        self.email = Email(email) if email else None
        self.coments = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))          

    def remove_phone(self, phone):
        self.phones.remove_phone(phone)

    def edit_phone(self, old_phone, new_phone):
        self.phones.edit_phone(old_phone, new_phone)        

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    # Методи для роботи з нотатками
    def add_comment(self, text):
        self.coments.append(text)

    def edit_comment(self, index, new_text):
        try:
            self.coments[index] = new_text
        except IndexError:
            return "Comment not found."

    def remove_comment(self, index):
        try:
            del self.coments[index]
        except IndexError:
            return "Comment not found."

    def list_note(self):
        return self.coments

    def find_note(self, text):
        return [note for note in self.coments if text.lower() in note.lower()]

    def get_details(self):
        details = f"Name: {self.name.value}\n"
        details += f"Phone: {', '.join([p.value for p in self.phones]) if self.phones else 'No phone number.'}\n"
        details += f"Address: {self.address.value if self.address else 'No address.'}\n"
        details += f"Email: {self.email.value if self.email else 'No email.'}\n"
        details += f"Birthday: {self.birthday.value.strftime('%d.%m.%Y') if self.birthday else 'Not provided'}\n"
        if self.coments:
            notes_str = "\n".join([f"{idx + 1}: {note}" for idx, note in enumerate(self.coments)])
            details += f"Comments:\n{notes_str}"
        return details


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
        return "Usage: edit [name] [phone(s) (optional)] [address (optional)] [email (optional)] [birthday (optional)]"
    
    name = args[0]
    additional_args = args[1:]

    phones = []
    address = None
    email = None
    birthday = None

    for arg in additional_args:
        if ',' in arg:  # Якщо аргумент містить кому, вважаємо, що це список телефонів
            phones.extend(arg.split(','))
        elif re.match(r"\d{2}\.\d{2}\.\d{4}", arg):  # Перевірка на формат дати DD.MM.YYYY
            birthday = arg
        elif re.match(r"[^@]+@[^@]+\.[^@]+", arg):  # Перевірка на формат email
            email = arg
        elif re.match(r"\d{10}", arg):  # Перевірка на один телефонний номер
            phones.append(arg)
        else:  # Все інше вважається адресою
            address = arg

    record = book.get_record(name)
    if not record:
        return "Record not found."

    if phones:
        record.phones = [Phone(phone) for phone in phones if re.match(r"\d{10}", phone)]  # Оновлення телефонних номерів, перевірка формату
    if address:
        record.address = Address(address)
    if email:
        record.email = Email(email)
    if birthday:
        record.birthday = Birthday(birthday)

    return f"Record for {name} has been updated."



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
def add_comment_command(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: add_comment [name] [comment_text]"
    name, comment_text = args[0], " ".join(args[1:])
    record = book.get_record(name)
    if record:
        record.add_comment(comment_text)
        return "Comment added."
    else:
        return "Record not found."

def remove_comment_command(args, book: AddressBook):
    if len(args) != 2 or not args[1].isdigit():
        return "Usage: remove-comment [name] [comment_index]"
    name, comment_index = args[0], int(args[1]) - 1  # Зверніть увагу на віднімання 1, щоб врахувати індексацію з нуля
    record = book.get_record(name)
    if record:
        result = record.remove_comment(comment_index)
        return result if result else "Comment removed."
    else:
        return "Record not found."

def edit_comment_command(args, book: AddressBook):
    if len(args) < 3 or not args[1].isdigit():
        return "Usage: edit_comment [name] [comment_index] [new_text]"
    name, comment_index, new_text = args[0], int(args[1]) - 1, " ".join(args[2:])
    record = book.get_record(name)
    if record:
        result = record.edit_comment(comment_index, new_text)
        return result if result else "Comment updated."
    else:
        return "Record not found."

def add_note_command(args, notes_dif: Notes):
    note_text = " ".join(args)
    notes_dif.add_note(note_text)
    return "Note added."

def edit_note_command(args, notes_dif: Notes):
    if len(args) < 2:
        return "Usage: edit-notes [note_id] [new_note]"

    try:
        note_id = int(args[0]) - 1  # Перетворення в індекс Python
        new_note = " ".join(args[1:])
        return notes_dif.edit_note(note_id, new_note)
    except ValueError:
        return "Invalid note ID."

def remove_note_command(args, notes_dif: Notes):
    try:
        note_id = int(args[0]) - 1  # Перетворення в індекс Python
        return notes_dif.remove_note(note_id)
    except ValueError:
        return "Invalid note ID."

def notes_command(args, notes_dif: Notes):
    return notes_dif.list_note_command()

def find_note_command(args, notes_dif: Notes):
    search_text = " ".join(args)
    return notes_dif.find_note_command(search_text)


def main():
    save_service = SaveService()
    book = AddressBook(save_service)
    notes_dif = Notes(save_service)

    commands = {
        "add": lambda args: add_contact_command(args, book),
        "edit": lambda args: edit_contact_command(args, book),
        "remove": lambda args: remove_contact_command(args, book),
        "birthdays": lambda args: birthdays_command(args, book),
        "hello": lambda args: hello_command(args),
        "all": lambda args: show_all_contacts_command(args, book),
        "search": lambda args: search_contacts_command(args, book),
        "add-comment": lambda args: add_comment_command(args, book),
        "remove-comment": lambda args: remove_comment_command(args, book),
        "edit-comment": lambda args: edit_comment_command(args, book),
        "add-note": lambda args: add_note_command(args, notes_dif),
        "remove-note": lambda args: remove_note_command(args, notes_dif),
        "edit-note": lambda args: edit_note_command(args, notes_dif),
        "notes": lambda args: notes_command(args, notes_dif),
        "find-note": lambda args: find_note_command(args, notes_dif),
        #"save-info": lambda _: "All information has been saved automatically."
    }

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").lower().split()
        if not user_input:                                       # Перевіряємо, чи список не порожній
            print("No command entered. Please try again.")
            continue 

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