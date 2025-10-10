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