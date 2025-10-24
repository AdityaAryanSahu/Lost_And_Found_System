from app.core.database import db
from app.models.image import ImageModel

collection = db["images"]

class ImageRepo:
    async def add_image(image: ImageModel):
        result = await collection.insert_one(image.to_dict())
        return str(result.inserted_id)

    async def get_images_by_item(item_id: str, limit: int = 20):
        return await collection.find({"item_id": item_id}).to_list(length=limit)

    async def delete_image(path: str):
        return await collection.delete_one({"path": path})
