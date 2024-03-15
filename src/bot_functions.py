from datetime import datetime, timedelta
from objects.Record import Record
from objects.AddressBook import AddressBook
from objects.Notes import Notes


def input_error(func):
    """
    Decorator function to handle input errors gracefully by returning the error message as a string.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: Decorated function.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return inner

@input_error
def add_contact_command(args, book: AddressBook):
    """
    Add a new contact to the address book.
    Args:
        args (list): List of arguments for the contact.
    Returns:
        str: Confirmation message indicating that the contact has been added.
    """
    if len(args) < 1:
        raise ValueError("Not enough arguments. Usage: add [name] [phone phone] [address (optional)] [email (optional)] [birthday (optional)]")

    name, *other_args = args  # Разделение аргументов на имя и остальные аргументы

    phones = []
    email = None
    birthday = None
    address = None

    for arg in other_args:
        if arg.isdigit() == True and len(arg) > 4:
            phones.append(arg)
        elif '@' in arg:  # Проверка на электронную почту
            email = arg
        elif '.' in arg and len(arg.split('.')) == 3:  # Проверка на дату
            try:
                datetime.strptime(arg, '%d.%m.%Y')  # Проверка формата даты
                birthday = arg
            except ValueError:
                print(f"Invalid date format for birthday: {arg}. Expected DD.MM.YYYY.")
        else:
            # Если аргумент не является ни датой, ни электронной почтой, то предполагаем, что это адрес
            if address is None:
                address = arg
            else:
                address += " " + arg  # Добавление аргумента к уже существующему адресу, если он есть

    record = Record(name, phones=phones, address=address, email=email, birthday=birthday)
    book.add_record(record)
    return "Contact added."

def birthdays_command(args, book: AddressBook):
    """
    Get upcoming birthdays from the address book.
    Args:
        args (list): List of arguments. Expected format: [number_of_days]
    Returns:
        str: Formatted list of upcoming birthdays or a message indicating no birthdays in the specified days.
    """
    if not args or not args[0].isdigit():
        return "Usage: birthdays [number_of_days]"
    days = int(args[0])
    birthdays_list = book.get_birthdays_in_next_days(days)
    if birthdays_list:
        formatted_birthdays = "\n".join([f"{birthday.strftime('%A: %d.%m.%Y')}: {name}" for name, birthday in birthdays_list])
        return formatted_birthdays
    else:
        return "No birthdays in the next specified days."

def search_contacts_command(args, book: AddressBook):
    """
    Search for contacts in the address book.
    Args:
        args (list): List of arguments. Expected format: [search_term]
    Returns:
        str: Result of the search.
    """
    if len(args) != 1:
        return "Usage: search [search_term]"
    search_term = args[0]
    return book.search_contacts(search_term)

def edit_contact_command(args, book: AddressBook):
    """
    Edit an existing contact in the address book.
    Args:
        args (list): List of arguments for editing the contact.
    Returns:
        str: Confirmation message indicating that the contact has been edited.
    """
    if len(args) < 1:
        return "Usage: edit [name] [phone (optional)] [address (optional)] [email (optional)] [birthday (optional)]"
    
    name, *other_args = args
    phones = []
    email = None
    address = None
    birthday = None
    
    for arg in other_args:
        if arg.isdigit() == True and len(arg) > 4:
            phones.append(arg)
        elif '@' in arg:  # Проверка на электронную почту
            email = arg
        elif '.' in arg and len(arg.split('.')) == 3:  # Проверка на дату
            try:
                datetime.strptime(arg, '%d.%m.%Y')  # Проверка формата даты
                birthday = arg
            except ValueError:
                print(f"Invalid date format for birthday: {arg}. Expected DD.MM.YYYY.")
        else:
            # Если аргумент не является ни датой, ни электронной почтой, то предполагаем, что это адрес
            if address is None:
                address = arg
            else:
                address += " " + arg  # Добавление аргумента к уже существующему адресу, если он есть
    
    return book.edit_record(name, phones, address, email, birthday)

def remove_contact_command(args, book: AddressBook):
    """
    Remove a contact from the address book.
    Args:
        args (list): List of arguments. Expected format: [name]
    Returns:
        str: Confirmation message indicating that the contact has been removed.
    """
    if len(args) != 1:
        return "Usage: remove [name]"
    name = args[0]
    return book.remove_record(name)

def hello_command(args):
    """
    Return a greeting message.
    Args:
        args (list): List of arguments. Not used in this function.
    Returns:
        str: Greeting message.
    """
    return "Hello! How can I assist you today?"

def show_all_contacts_command(args, book: AddressBook):
    """
    Returns a list of all contacts in the address book.
    Args:
        args: Function arguments (not used).
    Returns:
        str: List of all contacts.
    """
    return book.get_all_contacts()


def add_comment_command(args, book: AddressBook):
    """
    Adds a comment to the specified contact in the address book.
    Args:
        args (list): List of arguments. Expected format [name, comment_text].
    Returns:
        str: Message indicating the comment has been added.
    """
    if len(args) < 2:
        return "Usage: add_note [name] [comment_text]"
    name, note_text = args[0], " ".join(args[1:])
    return book.add_comment(name, note_text)
  

def remove_comment_command(args, book: AddressBook):
    """
    Removes a comment from the specified contact in the address book.
    Args:
        args (list): List of arguments. Expected format [name].
    Returns:
        str: Message indicating the comment has been removed.
    """
    if len(args) != 1:
        return "Usage: remove-note [name]"
    name = args[0]
    return book.remove_comment(name)
    

def add_notes_command(args, notes_dif: Notes):
    """
    Adds a note to the list of notes.
    Args:
        args (list): List of arguments. Expected note text.
    Returns:
        str: Message indicating the note has been added.
    """
    note_text = " ".join(args)
    notes_dif.add_notes(note_text)
    return "Note added."

def edit_notes_command(args, notes_dif: Notes):
    """
    Edits an existing note.
    Args:
        args (list): List of arguments. Expected format [note_id] [new_note].
    Returns:
        str: Message indicating the note has been edited.
    """
    if len(args) < 2:
        return "Usage: edit-notes [note_id] [new_note]"

    try:
        note_id = int(args[0]) - 1  # Перетворення в індекс Python
        new_note = " ".join(args[1:])
        return notes_dif.edit_notes(note_id, new_note)
    except ValueError:
        return "Invalid note ID."
    
def remove_notes_command(args, notes_dif: Notes):
    """
    Removes a note from the list by its identifier.
    Args:
        args (list): List of arguments. Expected format [note_id].
    Returns:
        str: Message indicating the note has been removed.
    """
    try:
        note_id = int(args[0]) - 1  # Перетворення в індекс Python
        return notes_dif.remove_notes(note_id)
    except ValueError:
        return "Invalid note ID."


def list_notes_command(args, notes_dif: Notes):
    """
    Returns a list of all notes.
    Args:
        args: Function arguments (not used).
    Returns:
        str: List of all notes.
    """
    return notes_dif.list_notes_command()

def find_notes_command(args, notes_dif: Notes):
    """
    Searches for notes containing the specified text.
    Args:
        args (list): List of arguments. Expected search text.
    Returns:
        str: List of found notes.
    """
    search_text = " ".join(args)
    return notes_dif.find_notes_command(search_text)

def help(commands_dict):
    """
    Display help information for available commands along with their docstrings.

    Args:
        commands_dict (dict): A dictionary mapping command names to their corresponding functions.

    Returns:
        None
    """
    commands_dict = {
    "add": add_contact_command,
    "edit": edit_contact_command,
    "remove": remove_contact_command,
    "birthdays": birthdays_command,
    "hello": hello_command,
    "all": show_all_contacts_command,
    "search": search_contacts_command,
    "add-comment": add_comment_command,
    "remove-comment": remove_comment_command,
    "add-note": add_notes_command,
    "remove-note": remove_notes_command,
    "edit-note": edit_notes_command,
    "notes": list_notes_command,
    "find-notes": find_notes_command
}
    for command, func in commands_dict.items():
        if hasattr(func, "__doc__") and func.__doc__:
            print(f"{command}:")
            print(func.__doc__.strip())
            print("*" * 100)