import pickle
import os.path


class SaveService:

    def save(self, key, data):
        with open(f'saves\\{key}.pickle', 'wb') as handle:
            pickle.dump(data, handle)
            
    
    def load(self, key):
        path = f'saves\\{key}.pickle'
        if not os.path.isfile(path):
            return None
        with open(f'saves\\{key}.pickle', 'rb') as handle:
            return pickle.load(handle)
   
            

