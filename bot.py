from classes import AddressBook, Record, BirthdayValidationError

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "You should add name of contact"
        except BirthdayValidationError:
            return "Invalid date format. Should be dd.mm.yyyy"

    return inner



def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts: AddressBook):  
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added."
    

@input_error
def change_contact(args, contacts):
    name, phone, new_phone = args
    record = contacts.find(name)
    if record: 
        record.edit_phone(phone, new_phone)
        return "Contact changed."
    else:
        return "Contact not found."
   

@input_error    
def phone_contact(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record: 
        return record
    else:
        return "Contact not found."

    
    
def show_all(contacts):
    if contacts:
        info = ''
        for name in contacts.values():
            info += f'Contact {name}\n'
        return info
    else:
        return "Contact list is empty"    
    
@input_error
def add_birthday(args, contacts: AddressBook):
    name, birthday = args
    record = contacts.find(name)
    if record: 
        record.add_birthday(birthday)
        return 'Birthday has been added'
    else:
        return 'Contact not found'
    

@input_error
def show_birthday(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record:
        if record.birthday:
            return record.birthday.value
        else:
            return 'This contact has unknown birthday'
    else:
        return 'Contact not found'
        

def birthdays(contacts: AddressBook):
    return contacts.get_birthdays_per_week()        


def main():
    contacts = AddressBook()
    contacts.load()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            contacts.save()
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(phone_contact(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))  
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()