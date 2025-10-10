from app.models.item import ItemCreation, ItemResponse, ItemList
from app.services.image_service import ImageService
from fastapi import status, UploadFile
from typing import Optional, List
from datetime import datetime
import uuid


class ItemService:
    
    def __init__(self):
        self.image_service=ImageService()
        
        
    async def create_item(self, item_cr: ItemCreation, image_files: List[UploadFile]) -> Optional[ItemResponse]:
        
        id=str(uuid.uuid4())
        
        image_metadata_list = []
        for file in image_files:

            image_meta = await self.image_service.process_and_upload_image(file, item_id=id)
            image_metadata_list.append(image_meta)
        
        item_bd= ItemResponse(
            user_id=item_cr.user_id,
            item_id=id,
            desc=item_cr.desc,
            img=image_metadata_list,
            type= item_cr.type,
            created_at=datetime.now(), 
            status=status.HTTP_201_CREATED,
            mssg="item created"
        )
        
        #push to database
        
        return item_bd

    async def get_all_items(self, limit: int = 10, offset: int = 0) -> ItemList:
        #get all items, create the response models and push to list
        item_list=ItemList()
        return item_list
    
    async def get_item_id(self, item_id:str)-> Optional[ItemResponse]:
        #check if item_id present in database, if not riase exception
        #if found create a response model item_got
        item_got=ItemResponse()
        return item_got
    
    async def delete_item(self, item_id:str)->bool:
        #search in database and delete
        #if not found return false else return true
        return False
        
    async def update_item(self, item_id:str, item_update: ItemCreation) -> Optional[ItemResponse]:
        
        #using data of item_update, for a particualr item_id update value in database
        return item_update
    
    async def mark_item_claimed(self, item_id: str) -> bool:

        #get item from db as existing_item= db.get(itemm_id)
        if not existing_item:
            return False
        
        # Simple mock update
        existing_item.is_claimed = True
        return True
