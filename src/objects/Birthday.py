from objects.Field import Field
from datetime import datetime

class Birthday(Field):
    def __init__(self, value):
        super().__init__(datetime.strptime(value, '%d.%m.%Y'))

    @property
    def date(self):
        return self.value.date()
