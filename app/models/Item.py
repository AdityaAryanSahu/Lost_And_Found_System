from pydantic import BaseModel
from typing import List
from Image import image


class ItemCreation(BaseModel):
    user_id: int #user id of the person found (reg_no)
    desc: str #colour and place 
    img: image  #image for the item
    type: str #type like bottle, pen etc
    
class ItemResponse(BaseModel):
    item_id:int
    mssg:str
    
class ItemList(BaseModel):
    item_list=List[ItemResponse]=[]

    count:int
