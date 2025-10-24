from typing import List

class MatchModel:
    def __init__(self, search_type: str, keywords: List[str], location: str, matched_item: dict):
        self.search_type = search_type
        self.keywords = keywords
        self.location = location
        self.matched_item = matched_item
        self.item_id = matched_item.get("item_id", None)
        self.mssg = "Match found."

    def to_dict(self):
        return {
            "search_type": self.search_type,
            "keywords": self.keywords,
            "location": self.location,
            "matched_item": self.matched_item,
            "item_id": self.item_id,
            "mssg": self.mssg
        }
