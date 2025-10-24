from app.core.database import db
from app.models.item import ItemModel

collection = db["items"]

class ItemRepo:
    async def create_item(item: ItemModel):
        result = await collection.insert_one(item.to_dict())
        return str(result.inserted_id)

    async def get_item_by_id(item_id: str):
        return await collection.find_one({"item_id": item_id})

    async def list_items(limit: int = 100, offset: int = 0):
        return await collection.find().skip(offset).limit(limit).to_list(length=limit)

    async def update_claim_status(item_id: str, is_claimed: bool):
        return await collection.update_one(
            {"item_id": item_id},
            {"$set": {"is_claimed": is_claimed}}
        )
    async def update_fields(item_id: str, update_data: dict):

        return await collection.update_one(
        {"item_id": item_id},
        {"$set": update_data}
    )
    
    async def delete_item(item_id: str):
        return await collection.delete_one({"item_id": item_id})
