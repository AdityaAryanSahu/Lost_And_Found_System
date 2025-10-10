from typing import Optional, Annotated, List
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, File, UploadFile,Form
from app.models.item import ItemCreation, ItemList, ItemResponse
from app.models.user import UserCreation, UserResponse
from app.api.dependencies import get_item_service, get_current_user
from app.services.item_service import ItemService
import json

item_router=APIRouter()

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid Item details JSON: {e}")
    
    item_cr.user_id = current_user.user_id
    item_md=await service.create_item(item_cr, image_files)
    if item_md.status != status.HTTP_201_CREATED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=item_md.mssg)
    return item_md

@item_router.get("/", response_model=ItemList)
async def list_all_items(service: Annotated[ItemService, Depends(get_item_service)], limit:int =10, offset:int = 0):
    res= await service.get_all_items(limit, offset)
    return res

@item_router.get("/{item_id}", response_model=ItemResponse)
async def get_specific_item(item_id:str, service: Annotated[ItemService, Depends(get_item_service)]):
    if item_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="NULL id value")
    
    item_res= await service.get_item_id(item_id)
    if item_res.status != status.HTTP_200_OK:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No item found")
    return item_res

@item_router.put("/{item_id}", response_model=ItemResponse)
async def item_update(item_id:str, item_cr:ItemCreation, service: Annotated[ItemService, Depends(get_item_service)]):
    if item_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="NULL id value")
    item_res=await service.update_item(item_id, item_cr)
    if item_res.status != status.HTTP_200_OK:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No item found")
    return item_res

@item_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def item_deletion(item_id:str, service: Annotated[ItemService, Depends(get_item_service)]):
    if item_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="NULL id value")
    return await service.delete_item(item_id)
    