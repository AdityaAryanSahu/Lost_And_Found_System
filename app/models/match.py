from pydantic import BaseModel
from typing import List
from app.schemas.item import ItemResponse

class MatchSearchRequest(BaseModel):
    search_type: str  
    keywords: List[str] #from desc
    location: str 

class MatchResponse(BaseModel):
    matched_item: ItemResponse
    item_id: str
    mssg:str
    
class MatchList(BaseModel):
    matches: List[MatchResponse] = []
    count: int