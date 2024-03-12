from objects.Field import Field
import re

class Email(Field):
    
    def validate(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise ValueError("Invalid email address.")
        
    def __init__(self, value):
        super().__init__(value)
        self.validate()
    
    

    
