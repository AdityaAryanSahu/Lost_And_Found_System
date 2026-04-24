from fastapi import APIRouter, Depends, status
from typing import Annotated, List
from app.models.match import MatchSearchRequest, MatchList, MatchResponse
from app.models.user import UserResponse
from app.services.match_service import MatchService
from app.api.dependencies import get_match_service, get_current_user


match_router = APIRouter()

@match_router.post("/", response_model=MatchList)
async def all_matches(
    search_request: MatchSearchRequest, 
    service: Annotated[MatchService, Depends(get_match_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)] 
):
    matches= await service.find_potential_matches(search_request)
    return matches

@match_router.get("/saved/{item_id}")
async def get_saved_item_matches(
    item_id: str,
    service: Annotated[MatchService, Depends(get_match_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)] 
):
   
    match_doc = await service.get_saved_matches(item_id)
    
    if not match_doc:
        return {"has_match": False, "matches": []}
        
    if "_id" in match_doc:
        match_doc["_id"] = str(match_doc["_id"])
        
    return {"has_match": True, "match_data": match_doc}