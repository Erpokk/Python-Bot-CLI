from objects.AddressBook import AddressBook
from objects.Note import Note
import bot_functions




def main():
    book = AddressBook()
    notes = Note()
    
    commands = {
        "add": lambda args: bot_functions.add_contact_command(args, book),
        "edit": lambda args: bot_functions.edit_contact_command(args, book),
        "remove": lambda args: bot_functions.remove_contact_command(args, book),       
        "birthdays": lambda args: bot_functions.birthdays_command(args, book),        
        "hello": lambda args: bot_functions.hello_command(args),
        "all": lambda args: bot_functions.show_all_contacts_command(args, book),
        "search": lambda args: bot_functions.search_contacts_command(args, book),
        "add-note": lambda args: bot_functions.add_note_command(args, book),
        "remove-note": lambda args: bot_functions.remove_note_command(args, book),
        "edit-note": lambda args: bot_functions.edit_note_command(args, book),
        "list-notes": lambda args: bot_functions.list_notes_command(args, book),
        "find-notes": lambda args: bot_functions.find_notes_command(args, book),
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