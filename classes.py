import os
import pickle
from collections import UserDict
from datetime import datetime
from typing import Any
from collections import defaultdict


class BirthdayValidationError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value
    

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        self.__value = self.validate(new_value)


    def validate(self, number):
        if len(number) != 10 or not number.isdigit():
            raise ValueError
        else:
            return number
        

class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value
    

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        self.__value = self.validate(new_value)


    def validate(self, birthday_date):
        date_obj = datetime.strptime(birthday_date, '%d.%m.%Y')
        current_day = datetime.now()
        if date_obj > current_day:
            raise BirthdayValidationError()
        else:
            return birthday_date
        


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


    def add_phone(self, phone):
        phone_object = Phone(phone)
        self.phones.append(phone_object)


    def remove_phone(self, phone):
        for ph_object in self.phones:
            if ph_object.value == phone:
                self.phones.remove(ph_object)


    def edit_phone(self, old_phone, new_phone):
        for ph_object in self.phones:
            if ph_object.value == old_phone:
                ph_object.value = new_phone
            

    def find_phone(self, phone):
        for ph_object in self.phones:
            if ph_object.value == phone:
                return ph_object


    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, {self.birthday.value if self.birthday else ''}"

class AddressBook(UserDict):
    filename = "adressbook.bin"


    def add_record(self, record):
        self.data[record.name.value] = record


    def find(self, name):
        record = self.data.get(name)
        return record
    

    def delete(self, name):
        record = self.data.get(name)
        if record:
            del self.data[name]


    def load(self):
        if os.path.exists(AddressBook.filename):
            with open(AddressBook.filename, 'rb') as file:
                self.data = pickle.load(file) 


    def save(self):
        with open(AddressBook.filename, 'wb') as file:
            pickle.dump(self.data, file)

        


    def get_birthdays_per_week(self): 
        birthday_persons = defaultdict(list)
        today = datetime.today().date()
        for user in self.data.values():
            name: str = user.name.value
            birthday_obj = user.birthday
            if birthday_obj is None:
                continue
            birthday = datetime.strptime(birthday_obj.value, '%d.%m.%Y').date()
            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year+1)
            delta_days = (birthday_this_year - today).days
            if delta_days < 7:
                weekday = birthday_this_year.weekday()
                if weekday in [5, 6, 0]:
                    birthday_persons['Monday'].append(name)
                elif weekday == 1:
                    birthday_persons['Tuesday'].append(name)
                elif weekday == 2:
                    birthday_persons['Wednesday'].append(name)
                elif weekday == 3:
                    birthday_persons['Thursday'].append(name)
                elif weekday == 4:
                    birthday_persons['Friday'].append(name)
        info = []
        for day, persons in birthday_persons.items():
            info.append(f'{day}: {" ".join(persons)}')  
        return info            
        



if __name__ == '__main__':
     # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday('09.03.2000')

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
    print(book.get_birthdays_per_week())    


    print('success')