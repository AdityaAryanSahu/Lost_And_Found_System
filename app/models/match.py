from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional, Dict, Any
from app.models.item import ItemResponse

class MatchModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[str] = Field(None, alias="_id")
    item_id_a: str                             
    item_id_b: str                             
    score: float
    matched_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)

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