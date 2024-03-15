from objects.Name import Name
from objects.Phone import Phone
from objects.Birthday import Birthday
from objects.Address import Address
from objects.Email import Email

class Record:
    def __init__(self, name, phones=None, birthday=None, address=None, email=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones] if phones else []
        self.birthday = Birthday(birthday) if birthday else None
        self.address = Address(address) if address else None
        self.email = Email(email) if email else None
        self.comment = ""

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

  
    def add_comment(self, text):
        self.comment = text

    def remove_comment(self):
        self.comment = ""

    def show_comment(self):
        return self.comment

    def get_details(self):
        details = f"Name: {self.name.value}\n"
        details += f"Phone: {', '.join([p.value for p in self.phones]) if self.phones else 'No phone number.'}\n"
        details += f"Address: {self.address.value if self.address else 'No address.'}\n"
        details += f"Email: {self.email.value if self.email else 'No email.'}\n"
        details += f"Birthday: {self.birthday.value.strftime('%d.%m.%Y') if self.birthday else 'Not provided'}\n"
        details += f"Comment: {self.comment}"
            
        return details
