# app/core/cache.py
from typing import Dict, Any

class CacheManager:
    def __init__(self):
        self.cache: Dict[str, Any] = {}

    def get(self, key: str):
        return self.cache.get(key)

    def set(self, key: str, value: Any):
        self.cache[key] = value

    def delete(self, key: str):
        if key in self.cache:
            del self.cache[key]

# create a global instance
cache_manager = CacheManager()
