from app.core.database import get_db
from app.models.item import ItemModel



class ItemRepo:
    async def create_item(self,item: ItemModel):
        db=get_db()
        collection = db["items"]
        result = await collection.insert_one(item.to_dict())
        return str(result.inserted_id)

    async def get_item_by_id(self,item_id: str):
        db=get_db()
        collection = db["items"]
        return await collection.find_one({"item_id": item_id})

    async def list_items(self,limit: int = 100, offset: int = 0):
        db=get_db()
        collection = db["items"]
        return await collection.find().skip(offset).limit(limit).to_list(length=limit)

    async def update_claim_status(self,item_id: str, is_claimed: bool):
        db=get_db()
        collection = db["items"]
        return await collection.update_one(
            {"item_id": item_id},
            {"$set": {"is_claimed": is_claimed}}
        )
    async def update_fields(self,item_id: str, update_data: dict):
        db=get_db()
        collection = db["items"]

        return await collection.update_one(
        {"item_id": item_id},
        {"$set": update_data}
    )
    
    async def delete_item(self,item_id: str):
        db=get_db()
        collection = db["items"]
        return await collection.delete_one({"item_id": item_id})
