from servises.SaveService import SaveService

class Note:
    def __init__(self, save_service: SaveService):
        self._save_service = save_service
