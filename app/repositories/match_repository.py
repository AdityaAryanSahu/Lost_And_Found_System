from app.core.database import db
from app.models.match import MatchModel

collection = db["matches"]
class MatchRepo:
    async def add_match(match: MatchModel):
        result = await collection.insert_one(match.to_dict())
        return str(result.inserted_id)

    async def get_all_matches(limit: int = 100, offset: int = 0):
        return await collection.find().skip(offset).limit(limit).to_list(length=limit)

    async def get_match_by_item(item_id: str):
        return await collection.find_one({"item_id": item_id})

    async def delete_match(item_id: str):
        return await collection.delete_one({"item_id": item_id})
    
    async def update_match_fields(item_id: str, update_data: dict):
   
        return await collection.update_one(
            {"item_id": item_id},
            {"$set": update_data}
        )
