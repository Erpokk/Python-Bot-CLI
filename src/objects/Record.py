from objects.Name import Name
from objects.Phone import Phone
from objects.Birthday import Birthday
from objects.Address import Address
from objects.Email import Email

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
