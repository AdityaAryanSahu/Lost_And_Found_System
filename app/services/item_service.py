from app.models.item import ItemCreation, ItemResponse, ItemList, ItemModel
from app.services.image_service import ImageService
from fastapi import status, UploadFile
from typing import Optional, List
from app.repositories import image_repository, item_repository
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

class ItemService:
    
    def __init__(self, 
                 image_service: ImageService,
                 item_repo: item_repository.ItemRepo,
                 image_repo: image_repository.ImageRepo):
        self.image_service = image_service
        self.item_repository = item_repo
        self.image_repository= image_repo
        
        
    async def create_item(self, item_cr: ItemCreation, image_files: List[UploadFile]) -> Optional[ItemResponse]:
        id = str(uuid.uuid4())
        
        image_metadata_list = []
        for file in image_files:
            try:
                image_meta = await self.image_service.process_and_upload_image(file, item_id=id)
                image_metadata_list.append(image_meta)
            except Exception as e:
                logger.error(f"Error processing image: {e}")
                raise
        
        item_model = item_cr.to_model(
            item_id=id, 
            image_metadata=image_metadata_list, 
            created_at=datetime.now()
        )
        
        await self.item_repository.create_item(item_model)
        
        return ItemResponse.from_model(item_model)

    async def get_all_items(self, limit: int = 10, offset: int = 0) -> ItemList:
        try:
            item_models_list = await self.item_repository.list_items(limit, offset)
            items = []
            
            for m in item_models_list:
                try:
                    # Convert MongoDB ObjectId to string
                    if '_id' in m and not isinstance(m['_id'], str):
                        m['_id'] = str(m['_id'])
                    
                    # ✅ FETCH IMAGES FROM SEPARATE COLLECTION
                    item_id = m.get('item_id')
                    if item_id and self.image_repository:
                        images = await self.image_repository.get_images_by_item(item_id)
                        logger.info(f"Fetched {len(images)} images for item {item_id}")
                        # Replace embedded images with fetched images
                        m['images'] = images
                    else:
                        m['images'] = []
                    
                    item_model = ItemModel.model_validate(m, from_attributes=True)
                    item_response = ItemResponse.from_model(item_model)
                    items.append(item_response)
                    
                except Exception as e:
                    logger.error(f"Error parsing item document {m.get('_id', 'unknown')}: {e}", exc_info=True)
                    # Skip this item and continue with others
                    continue
            
            return ItemList(item_list=items, count=len(items))
            
        except Exception as e:
            logger.error(f"Error in get_all_items: {e}", exc_info=True)
            raise
    
    async def get_item_id(self, item_id: str) -> Optional[ItemResponse]:
        try:
            item_doc = await self.item_repository.get_item_by_id(item_id)
            
            if item_doc:
                # Convert MongoDB ObjectId to string
                if '_id' in item_doc and not isinstance(item_doc['_id'], str):
                    item_doc['_id'] = str(item_doc['_id'])
                
                # ✅ FETCH IMAGES FROM SEPARATE COLLECTION
                if self.image_repository:
                    images = await self.image_repository.get_images_by_item(item_id)
                    logger.info(f"Fetched {len(images)} images for item {item_id}")
                    item_doc['images'] = images
                else:
                    item_doc['images'] = []
                
                item_model = ItemModel.model_validate(item_doc, from_attributes=True)
                return ItemResponse.from_model(item_model)
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching item {item_id}: {e}", exc_info=True)
            raise

    
    async def delete_item(self, item_id: str) -> bool:
        try:
            result = await self.item_repository.delete_item(item_id)
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting item {item_id}: {e}", exc_info=True)
            raise
        
    async def update_item(self, item_id: str, item_update: ItemCreation) -> Optional[ItemResponse]:
        try:
            update_data = item_update.model_dump(exclude_unset=True)
            update_result = await self.item_repository.update_fields(item_id, update_data)
            
            # Return updated item
            return await self.get_item_id(item_id)
        except Exception as e:
            logger.error(f"Error updating item {item_id}: {e}", exc_info=True)
            raise
    
    async def mark_item_claimed(self, item_id: str) -> bool:
        try:
            result = await self.item_repository.update_claim_status(item_id, is_claimed=True)
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error marking item {item_id} as claimed: {e}", exc_info=True)
            raise
    
    async def update_item_with_images(self, item_id: str, item_cr: ItemCreation, image_files: List[UploadFile]) -> Optional[ItemResponse]:
        """Update item with new images"""
        try:
            # Process and upload new images
            image_metadata_list = []
            for file in image_files:
                try:
                    image_meta = await self.image_service.process_and_upload_image(file, item_id=item_id)
                    image_metadata_list.append(image_meta)
                except Exception as e:
                    logger.error(f"Error processing image: {e}")
                    raise
            
            # Update item with new image metadata
            item_model = item_cr.to_model(
                item_id=item_id,
                image_metadata=image_metadata_list,
                created_at=datetime.now()
            )
            
            # Update in repository
            await self.item_repository.update_fields(item_id, item_model.to_dict())
            
            # Return updated item
            return await self.get_item_id(item_id)
            
        except Exception as e:
            logger.error(f"Error updating item with images: {e}")
            raise
