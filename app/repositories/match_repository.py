from app.core.database import get_db
from app.models.match import MatchModel


class MatchRepo:
    async def add_match(self,match: MatchModel):
        db=get_db()
        collection = db["matches"]
        result = await collection.insert_one(match.to_dict())
        return str(result.inserted_id)

    async def get_all_matches(self,limit: int = 100, offset: int = 0):
        db=get_db()
        collection = db["matches"]
        return await collection.find().skip(offset).limit(limit).to_list(length=limit)

    async def get_match_by_item(self,item_id: str):
        db=get_db()
        collection = db["matches"]
        return await collection.find_one({"item_id": item_id})

    async def delete_match(self,item_id: str):
        db=get_db()
        collection = db["matches"]
        return await collection.delete_one({"item_id": item_id})
    
    async def update_match_fields(self,item_id: str, update_data: dict):
        db=get_db()
        collection = db["matches"]
        return await collection.update_one(
            {"item_id": item_id},
            {"$set": update_data}
        )
