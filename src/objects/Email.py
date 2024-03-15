from objects.Field import Field
import re

class Email(Field):
    """
    Represents an email field.

    Args:
        value (str): The email address to be validated and stored.

    Methods:
        validate(): Validates the email address format.
        __init__(value): Initializes the Email object with the given value and validates it.
    """
    
    def validate(self):
        """
        Validates the email address format.

        Raises:
            ValueError: If the email address format is invalid.
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise ValueError("Invalid email address.")
        
    def __init__(self, value):
        """
        Initializes the Email object with the given value and validates it.

        Args:
            value (str): The email address to be validated and stored.

        Raises:
            ValueError: If the email address format is invalid.
        """
        super().__init__(value)
        self.validate()