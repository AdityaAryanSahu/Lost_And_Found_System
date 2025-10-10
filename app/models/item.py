from pydantic import BaseModel
from typing import List
from .  image import Image
from typing import Optional
from datetime import datetime


class ItemCreation(BaseModel):
    user_id: str #user id of the person found (reg_no)
    desc: str #colour and place 
    img: List[Image] = []
    type: str #type like bottle, pen etc
    
class ItemResponse(BaseModel):
    user_id: str
    item_id:str
    desc: str
    img: List[Image] = []
    is_claimed: bool= False
    type: str
    created_at: Optional[datetime] = None
    status=int
    mssg:str
    
class ItemList(BaseModel):
    item_list=List[ItemResponse]=[]
    count:int