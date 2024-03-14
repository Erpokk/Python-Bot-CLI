
class SaveService:
    def __init__(self):
        self.storage = {}

    def save(self, key, data):
        self.storage[key] = data
    
    def load(self, key):
        return self.storage.get(key, None)
    
#     def __init__(self, filename='data.json'):
#         self.filename = filename
#         self.storage = self.load_from_file()

#     def save(self, key, data):
#         self.storage[key] = data
#         self.save_to_file()

#     def load(self, key):
#         return self.storage.get(key, None)

#     def save_to_file(self):
#         with open(self.filename, 'w') as f:
#             json.dump(self.storage, f)

#     def load_from_file(self):
#         if os.path.exists(self.filename):
#             with open(self.filename, 'r') as f:
#                 return json.load(f)
#         return {}
