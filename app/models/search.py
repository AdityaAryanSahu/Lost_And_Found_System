
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.item import ItemList 

class SearchRequest(BaseModel):
    query: Optional[str]= None
    item_type: Optional[str] = None
    location: Optional[str] = None
    date_from: Optional[datetime] = None
    is_claimed: Optional[bool] = False
    limit: int = 20
    offset: int = 0