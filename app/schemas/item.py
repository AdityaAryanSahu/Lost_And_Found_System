from datetime import datetime
from typing import List

class ItemModel:
    def __init__(self, user_id: str, desc: str, img: List[dict], type: str):
        self.user_id = user_id
        self.desc = desc
        self.img = img  # List of image dicts
        self.type = type
        self.is_claimed = False
        self.created_at = datetime.utcnow()
        self.status = 1  # active by default
        self.mssg = "Item successfully created."

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "desc": self.desc,
            "img": self.img,
            "type": self.type,
            "is_claimed": self.is_claimed,
            "created_at": self.created_at,
            "status": self.status,
            "mssg": self.mssg
        }
