from datetime import datetime
from objects.Phone import Phone
from objects.Birthday import Birthday
from objects.Address import Address
from objects.Email import Email
from servises.SaveService import SaveService

class AddressBook:
    name_for_save = "book"
    
    def __init__(self, save_service: SaveService):
        self._save_service = save_service
        
        loaded_data = save_service.load(AddressBook.name_for_save)
        if loaded_data == None:
            self._records = {}
        else:
            self._records = loaded_data
        

    def add_record(self, record):
        self._records[record.name.value] = record
        self._save_service.save(AddressBook.name_for_save, self._records)

    def add_record(self, record):
        self._records[record.name.value] = record

    def get_all_contacts(self):
        return "\n\n".join([record.get_details() for name, record in self._records.items()])

    def get_birthdays_in_next_days(self, days):
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
                
            self._save_service.save(AddressBook.name_for_save, self._records)
            return f"Record for {name} has been updated."
        else:
            return "Record not found."

    def remove_record(self, name):
        if name in self._records:
            del self._records[name]
            self._save_service.save(AddressBook.name_for_save, self._records)
            return f"Record for {name} has been removed."
        else:
            return "Record not found."
        
    def add_comment(self, name, comment):
        record = self.get_record(name)
        if record:
            record.add_comment(comment)
            self._save_service.save(AddressBook.name_for_save, self._records)
            return "Comment added."
        else:
            return "Record not found."
        
    def remove_comment(self, name):
        record = self.get_record(name)
        if record:
            record.remove_comment()
            self._save_service.save(AddressBook.name_for_save, self._records)
            return "Comment removed."
        else:
            return "Record not found."
