from datetime import datetime
from objects.Phone import Phone
from objects.Birthday import Birthday
from objects.Address import Address
from objects.Email import Email
from servises.SaveService import SaveService

class AddressBook:
    """
    Represents an address book.

    This class manages a collection of records, each representing a contact.
    It provides methods for adding, retrieving, updating, and removing contacts.
    """

    name_for_save = "book"
    
    def __init__(self, save_service: SaveService):
        """
        Initialize an AddressBook instance.

        Args:
            save_service (SaveService): The service used for saving and loading data.

        Returns:
            None
        """
        self._save_service = save_service
        
        loaded_data = save_service.load(AddressBook.name_for_save)
        if loaded_data == None:
            self._records = {}
        else:
            self._records = loaded_data

    def get_record(self, name):
        """
        Retrieve a record from the address book.

        Args:
            name (str): The name of the contact to retrieve.

        Returns:
            Record or None: The record corresponding to the provided name, or None if not found.
        """
        return self._records.get(name)  

    def add_record(self, record):
        """
        Add a new record to the address book.

        Args:
            record (Record): The record to add.

        Returns:
            None
        """
        self._records[record.name.value] = record
        self._save_service.save(AddressBook.name_for_save, self._records)

    def get_all_contacts(self):
        """
        Get details of all contacts in the address book.

        Returns:
            str: A formatted string containing details of all contacts.
        """
        return "\n\n".join([record.get_details() for name, record in self._records.items()])

    def get_birthdays_in_next_days(self, days):
        """
        Get upcoming birthdays within a specified number of days.

        Args:
            days (int): The number of days to consider for upcoming birthdays.

        Returns:
            list: A list of tuples containing names and birthday dates of contacts with upcoming birthdays.
        """
        today = datetime.now().date()
        upcoming_birthdays = []
        for record in self._records.values():
            if record.birthday:
                birthday_date = record.birthday.date
                next_birthday = birthday_date.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)
                days_until_birthday = (next_birthday - today).days
                if 0 <= days_until_birthday <= days:
                    upcoming_birthdays.append((record.name.value, next_birthday))
                
        return upcoming_birthdays
    
    def search_contacts(self, search_term):
        """
        Search for contacts based on a search term.

        Args:
            search_term (str): The term to search for in contact names, phone numbers, addresses, and emails.

        Returns:
            str: A formatted string containing details of contacts matching the search term.
        """
        results = []
        for name, record in self._records.items():
            if (search_term.lower() in name.lower() or
                any(search_term in phone.value for phone in record.phones) or
                (record.address and search_term.lower() in record.address.value.lower()) or
                (record.email and search_term.lower() in record.email.value.lower())):
                
                results.append(record.get_details())
                
        return "\n\n".join(results) if results else "No matching contacts found."

    def edit_record(self, name, phones=[], address=None, email=None, birthday=None):
        """
        Edit an existing record in the address book.

        Args:
            name (str): The name of the contact to edit.
            phones (list): List of new phone numbers.
            address (str): New address.
            email (str): New email.
            birthday (str): New birthday.

        Returns:
            str: A message indicating the result of the edit operation.
        """
        if name in self._records:
            record = self._records[name]
            if len(phones) > 0:
                record.phones = [Phone(phone) for phone in phones]
            if address:
                record.address = Address(address)
            if email:
                record.email = Email(email)
            if birthday:
                record.birthday = Birthday(birthday)
                
            self._save_service.save(AddressBook.name_for_save, self._records)
            return f"Record for {name} has been updated."
        else:
            return "Record not found."

    def remove_record(self, name):
        """
        Remove a record from the address book.

        Args:
            name (str): The name of the record to remove.

        Returns:
            str: A message indicating the result of the removal operation.
        """
        if name in self._records:
            del self._records[name]
            self._save_service.save(AddressBook.name_for_save, self._records)
            return f"Record for {name} has been removed."
        else:
            return "Record not found."
        
    def add_comment(self, name, comment):
        """
        Add a comment to a record in the address book.

        Args:
            name (str): The name of the record to add a comment to.
            comment (str): The comment to add.

        Returns:
            str: A message indicating the result of the comment addition operation.
        """
        record = self.get_record(name)
        if record:
            record.add_comment(comment)
            self._save_service.save(AddressBook.name_for_save, self._records)
            return "Comment added."
        else:
            return "Record not found."
        
    def remove_comment(self, name):
        """
        Remove a comment from a record in the address book.

        Args:
            name (str): The name of the contact whose comment needs to be removed.

        Returns:
            str: A message indicating whether the comment was successfully removed or if the record was not found.
        """
        record = self.get_record(name)
        if record:
            record.remove_comment()
            self._save_service.save(AddressBook.name_for_save, self._records)
            return "Comment removed."
        else:
            return "Record not found."
