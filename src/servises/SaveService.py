import pickle
import os.path


class SaveService:
    """
    Service class for saving and loading data using pickle serialization.

    Methods:
        save: Saves data to a file using pickle serialization.
        load: Loads data from a file using pickle deserialization.
    """
    def save(self, key, data):
        """
        Saves data to a file using pickle serialization.

        Args:
            key (str): The key or identifier for the data being saved.
            data: The data to be saved.
        """
        with open(f'saves\\{key}.pickle', 'wb') as handle:
            pickle.dump(data, handle)
            
    
    def load(self, key):
        """
        Loads data from a file using pickle deserialization.

        Args:
            key (str): The key or identifier for the data being loaded.

        Returns:
            Any: The loaded data, or None if the file does not exist.
        """
        path = f'saves\\{key}.pickle'
        if not os.path.isfile(path):
            return None
        with open(f'saves\\{key}.pickle', 'rb') as handle:
            return pickle.load(handle)
   
            

