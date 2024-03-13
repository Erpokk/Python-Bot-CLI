from datetime import datetime
from objects.Name import Name
from objects.Phone import Phone
from objects.Birthday import Birthday
from objects.Address import Address
from objects.Email import Email

class AddressBook:
    def __init__(self):
        self._records = {}

    def add_record(self, record):
        self._records[record.name.value] = record

    def get_record(self, name):
        return self._records.get(name)

    def get_all_contacts(self):
        return "\n\n".join([record.get_details() for name, record in self._records.items()])

    def get_birthdays_in_next_days(self, days):
        today = datetime.now().date()
        upcoming_birthdays = dict(list)
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
