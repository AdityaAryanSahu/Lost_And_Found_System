from typing import Optional, Annotated, List
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, File, UploadFile, Form
from app.models.item import ItemCreation, ItemList, ItemResponse
from app.models.user import UserResponse
from app.api.dependencies import get_item_service, get_current_user
from app.services.item_service import ItemService
import json
import logging

logger = logging.getLogger(__name__)

item_router = APIRouter()

@item_router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def item_create(
    item_json: Annotated[str, Form(description="Item details in JSON format")],
    image_files: Annotated[List[UploadFile], File(description="One or more image files for the item")],
    service: Annotated[ItemService, Depends(get_item_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    try:
        item_cr = ItemCreation(**json.loads(item_json))
    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid Item details JSON: {e}"
        )
    
    item_cr.user_id = current_user.user_id
    try:
        item_md = await service.create_item(item_cr, image_files)
        return item_md
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create item: {str(e)}"
        )

@item_router.get("/", response_model=ItemList)
async def list_all_items(
    service: Annotated[ItemService, Depends(get_item_service)],
    limit: int = 100,
    offset: int = 0
):
    res = await service.get_all_items(limit, offset)
    return res

@item_router.get("/{item_id}", response_model=ItemResponse)
async def get_specific_item(
    item_id: str,
    service: Annotated[ItemService, Depends(get_item_service)]
):
    if item_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="NULL id value"
        )
    
    item_res = await service.get_item_id(item_id)
    if item_res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No item found"
        )
    
    return item_res


@item_router.put("/{item_id}", response_model=ItemResponse)
async def item_update(
    item_id: str,
    item_json: Annotated[str, Form(description="Item details in JSON format")],
    service: Annotated[ItemService, Depends(get_item_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    image_files: Annotated[List[UploadFile] | None, File(description="Optional new images")] = None,  # ✅ At the end
):
    """Update an existing item"""
    if item_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="NULL id value"
        )
    
    # Parse JSON from form data
    try:
        item_data = ItemCreation(**json.loads(item_json))
    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid Item details JSON: {e}"
        )
    
    # Get existing item to check ownership
    existing_item = await service.get_item_id(item_id)
    if existing_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    # Check if user owns this item
    if existing_item.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own items"
        )
    
    # Update item
    try:
        if image_files and len(image_files) > 0:
            # Update with new images
            item_res = await service.update_item_with_images(item_id, item_data, image_files)
        else:
            # Update without changing images
            item_res = await service.update_item(item_id, item_data)
        
        if item_res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Failed to update item"
            )
        
        return item_res
    except Exception as e:
        logger.error(f"Error updating item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update item: {str(e)}"
        )

@item_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def item_deletion(
    item_id: str,
    service: Annotated[ItemService, Depends(get_item_service)]
):
    if item_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="NULL id value"
        )
    
    return await service.delete_item(item_id)

@item_router.patch("/{item_id}/claim", response_model=ItemResponse)
async def mark_item_as_claimed(
    item_id: str,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    item_service: Annotated[ItemService, Depends(get_item_service)]
):
    """Mark an item as claimed (only by owner)"""
    if item_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="NULL id value"
        )
    
    item = await item_service.get_item_id(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    if item.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the item owner can mark it as claimed"
        )
    
    try:
        await item_service.item_repository.update_claim_status(item_id, True)
        updated_item = await item_service.get_item_id(item_id)
        if updated_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Failed to fetch updated item"
            )
        return updated_item
    except Exception as e:
        logger.error(f"Error updating claim status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update claim status: {str(e)}"
        )
