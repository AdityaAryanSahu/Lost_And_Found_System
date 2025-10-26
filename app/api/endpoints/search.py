
from fastapi import APIRouter, Depends, status
from typing import Annotated
from app.models.search import SearchRequest
from app.models.user import UserResponse
from app.models.item import ItemList
from app.api.dependencies import get_current_user, get_search_service
from app.services.search_service import SearchService 

search_router = APIRouter()


@search_router.post("/", response_model=ItemList)
async def advanced_search_endpoint(
    search_request: SearchRequest, 
    service: Annotated[SearchService, Depends(get_search_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)] 
):
   
    
    results = await service.search_items(search_request)
    return results