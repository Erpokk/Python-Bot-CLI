from objects.Field import Field
from datetime import datetime

class Birthday(Field):
    """
    Represents the birthday of a contact.

    Args:
        value (str): The string representation of the birthday in the format 'DD.MM.YYYY'.

    Attributes:
        str_data (str): The string representation of the birthday.
        date (datetime.date): The birthday date.

    Methods:
        __init__(value): Initializes the Birthday object with the given value.
    """

    def __init__(self, value):
        """
        Initializes the Birthday object.

        Args:
            value (str): The string representation of the birthday in the format 'DD.MM.YYYY'.
        """
        super().__init__(datetime.strptime(value, '%d.%m.%Y'))
        self.str_data = value

    @property
    def date(self):
        """
        Returns the birthday date.

        Returns:
            datetime.date: The birthday date.
        """
        return self.value.date()