from objects.Name import Name
from objects.Phone import Phone
from objects.Birthday import Birthday
from objects.Address import Address
from objects.Email import Email

class Record:
    """
    Represents a contact record.

    Attributes:
        name (Name): The name of the contact.
        phones (list of Phone): List of phone numbers associated with the contact.
        birthday (Birthday): The birthday of the contact.
        address (Address): The address of the contact.
        email (Email): The email address of the contact.
        comment (str): Additional comments or notes about the contact.

    Methods:
        add_phone: Adds a new phone number to the contact.
        remove_phone: Removes a phone number from the contact.
        edit_phone: Edits an existing phone number of the contact.
        add_birthday: Adds a birthday to the contact.
        add_comment: Adds a comment or note to the contact.
        remove_comment: Removes the comment or note from the contact.
        show_comment: Retrieves the comment or note of the contact.
        get_details: Retrieves the details of the contact as a formatted string.
    """
    def __init__(self, name, phones=None, birthday=None, address=None, email=None):
        """
        Initializes a Record instance.

        Args:
            name (str): The name of the contact.
            phones (list of str, optional): List of phone numbers associated with the contact.
            birthday (str, optional): The birthday of the contact.
            address (str, optional): The address of the contact.
            email (str, optional): The email address of the contact.
        """
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones] if phones else []
        self.birthday = Birthday(birthday) if birthday else None
        self.address = Address(address) if address else None
        self.email = Email(email) if email else None
        self.comment = ""

    def add_phone(self, phone):
        """
        Adds a new phone number to the contact.

        Args:
            phone (str): The phone number to add.

        Raises:
            ValueError: If the phone number already exists for the contact.
        """
        if any(phone.value == p.value for p in self.phones):
            raise ValueError("Phone number already exists for this contact")
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """
        Removes a phone number from the contact.

        Args:
            phone (str): The phone number to remove.
        """
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        """
        Edits an existing phone number of the contact.

        Args:
            old_phone (str): The current phone number to be edited.
            new_phone (str): The new phone number.

        Returns:
            str: Confirmation message indicating the phone number update status.
        """
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return "Phone number updated."
        return "Phone not found."

    def add_birthday(self, birthday):
        """
        Adds a birthday to the contact.

        Args:
            birthday (str): The birthday to add.
        """
        self.birthday = Birthday(birthday)

  
    def add_comment(self, text):
        """
        Adds a comment or note to the contact.

        Args:
            text (str): The comment or note to add.
        """
        self.comment = text

    def remove_comment(self):
        """Removes the comment or note from the contact."""
        self.comment = ""

    def show_comment(self):
        """
        Retrieves the comment or note of the contact.

        Returns:
            str: The comment or note.
        """
        return self.comment

    def get_details(self):
        """
        Retrieves the details of the contact as a formatted string.

        Returns:
            str: The formatted details of the contact.
        """
        details = f"Name: {self.name.value}\n"
        details += f"Phone: {', '.join([p.value for p in self.phones]) if self.phones else 'No phone number.'}\n"
        details += f"Address: {self.address.value if self.address else 'No address.'}\n"
        details += f"Email: {self.email.value if self.email else 'No email.'}\n"
        details += f"Birthday: {self.birthday.value.strftime('%d.%m.%Y') if self.birthday else 'Not provided'}\n"
        details += f"Comment: {self.comment}"
            
        return details
