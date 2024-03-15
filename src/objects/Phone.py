from objects.Field import Field

class Phone(Field):
    """
    Represents a phone number field.

    Methods:
        __init__: Initializes a Phone instance with a value.
        validate: Validates the phone number format.
    """
    def __init__(self, value):
        """
        Initializes a Phone instance with a value.

        Args:
            value (str): The phone number value.
        """
        super().__init__(value)
        self.validate()

    def validate(self):
        """
        Validates the phone number format.

        Raises:
            ValueError: If the phone number format is invalid.
        """
        if not self.value.isdigit() or len(self.value) != 10:
            raise ValueError("Phone number must consist of 10 digits.")
