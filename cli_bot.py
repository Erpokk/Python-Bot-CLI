
from classes import AddressBook, Record, DateFormatException
 
def input_error(func):   
    def inner(*args, **kwargs):   
        try:
            return func(*args, **kwargs)
        except DateFormatException:
            return "Incorrect format or future date. Use format Day/Month/Year (Ex. 01/01/2000)."
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Given key not found"
        except IndexError:
            return "Index out of range"
        # except Exception:
        #     return "Other Error"

    return inner

@input_error
def parse_input(user_input):    
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def change_contact(args, book):
    name, new_phone = args
    record = book.find(name)
    if record != "Not found":
        result = record.edit_phone(record.phones[0].value, new_phone)                
        if result == "Phone successfully changed":
            return "Update."
        else:
            return result
    else:
        return f"Contact {name} not found."

@input_error
def show_all(book):
    all_contacts = []
    for record in book.data.values():
        all_contacts.append(str(record))
    return "\n".join(all_contacts)

@input_error
def birthdays(book):
    result = book.get_birthdays_per_week()
    return result if result else ""
    
@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record != "Not found":
        return record.birthday.value.strftime('%d.%m.%Y')
    else:
        return f"Contact {name} not found."

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record != "Not found":
        return record.phones[0].__str__()
    else:
        return f"Contact {name} not found."

@input_error
def add_contact(args, book):
    name, phone = args
    if book.find(name) == "Not found":
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    else:
        return "This contact is already in contacts. Use command 'change'."

@input_error    
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record != "Not found":
        record.add_birthday(birthday)
        return "Birthday added." 
    else:
        return f"Contact {name} not found"


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
