from datetime import datetime

class ImageModel:
    def __init__(self, item_id: str, path: str):
        self.item_id = item_id
        self.path = path
        self.date_uploaded = datetime.utcnow()

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "path": self.path,
            "date_uploaded": self.date_uploaded
        }
