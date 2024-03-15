class Field:
    """
    Represents a generic field.

    Attributes:
        value: The value stored in the field.

    Methods:
        __init__(value): Initializes the Field object with the given value.
    """
    def __init__(self, value):
        """
        Initializes the Field object with the given value.

        Args:
            value: The value to be stored in the field.
        """
        self.value = value