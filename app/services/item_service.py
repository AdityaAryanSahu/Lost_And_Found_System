from app.models.item import ItemCreation, ItemResponse, ItemList, ItemModel
from app.services.image_service import ImageService
from fastapi import status, UploadFile, Depends
from typing import Optional, List, Annotated
from app.repositories import image_repository
from datetime import datetime
import uuid


class ItemService:
    
    def __init__(self, 
                 image_service: Annotated[ImageService, Depends()],
                 item_repo: image_repository):
        self.image_service = image_service
        self.item_repository = item_repo
        
        
    async def create_item(self, item_cr: ItemCreation, image_files: List[UploadFile]) -> Optional[ItemResponse]:
        
        id=str(uuid.uuid4())
        
        image_metadata_list = []
        for file in image_files:

            image_meta = await self.image_service.process_and_upload_image(file, item_id=id)
            image_metadata_list.append(image_meta)
        item_model = item_cr.to_model(item_id=id, image_metadata=image_metadata_list, created_at=datetime.now())
        
        await self.item_repository.create_item(item_model)
        
        return ItemResponse.from_model(item_model)

    async def get_all_items(self, limit: int = 10, offset: int = 0) -> ItemList:
        item_models_list = await self.item_repository.list_items(limit, offset)
        items = [ItemResponse.from_model(ItemModel(**m)) for m in item_models_list]
        return ItemList(items=items, count=len(items))
    
    async def get_item_id(self, item_id:str)-> Optional[ItemResponse]:
        item_doc = await self.item_repository.get_item_by_id(item_id)
        if item_doc:
            item_model = ItemModel(**item_doc)
            return ItemResponse.from_model(item_model)
        return None
    
    async def delete_item(self, item_id:str)->bool:
        result = await self.item_repository.delete_item(item_id)
        return result.deleted_count > 0
        
    async def update_item(self, item_id:str, item_update: ItemCreation) -> Optional[ItemResponse]:
        
        update_data = item_update.model_dump(exclude_unset=True)
       
        update_result = await self.item_repository.update_item_fields(item_id, update_data)
     
        if update_result and update_result.modified_count > 0:

            return await self.get_item_id(item_id)
        
  
        return await self.get_item_id(item_id)
    
    async def mark_item_claimed(self, item_id: str) -> bool:

        result = await self.item_repository.update_claim_status(item_id, is_claimed=True)
        return result.modified_count > 0
