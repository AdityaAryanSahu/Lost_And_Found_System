from app.core.database import get_db
from app.models.image import ImageModel



class ImageRepo:
    async def add_image(self,image: ImageModel):
        db=get_db()
        collection = db["images"]
        result = await collection.insert_one(image.to_dict())
        return str(result.inserted_id)

    async def get_images_by_item(self,item_id: str, limit: int = 20):
        db = get_db()
        collection = db["images"]
    
        images = await collection.find({"item_id": item_id}).to_list(length=limit)
    
    # Convert MongoDB documents to Image DTOs
        image_list = []
        for img in images:
        # MongoDB returns url, not path
            url = img.get("url") or img.get("path")
            image_dto = {
                "item_id": img["item_id"],
                "url": url,
                "date_uploaded": img["date_uploaded"]
            }
            image_list.append(image_dto)
    
        return image_list

    async def delete_image(self,path: str):
        db=get_db()
        collection = db["images"]
        return await collection.delete_one({"path": path})
