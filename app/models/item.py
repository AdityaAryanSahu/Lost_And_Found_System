from pydantic import BaseModel, Field
from typing import List
from .  image import Image
from typing import Optional, Dict, Any
from datetime import datetime

class ItemModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    
    item_id: str
    user_id: str                              
    desc: str
    images: List[Image] = Field(default_factory=list)
    type: str
    is_claimed: bool = False
    created_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)
    
class ItemCreation(BaseModel):
    user_id: str #user id of the person found (reg_no)
    desc: str #colour and place 
    img: List[Image] = []
    type: str #type like bottle, pen etc
    def to_model(self, item_id: str, image_metadata: List[Image], created_at: datetime) -> ItemModel:
        return ItemModel(
            item_id=item_id,
            user_id=self.user_id,
            desc=self.desc,
            images=image_metadata,
            type=self.type,
            created_at=created_at
        )
    
class ItemResponse(BaseModel):
    user_id: str
    item_id:str
    desc: str
    img: List[Image] = []
    is_claimed: bool= False
    type: str
    created_at: Optional[datetime] = None
    status: int
    mssg:str
    @classmethod
    def from_model(cls, item_model: ItemModel) -> 'ItemResponse':
        return cls(
            item_id=item_model.item_id,
            user_id=item_model.user_id,
            desc=item_model.desc,
            images=item_model.images,
            type=item_model.type,
            is_claimed=item_model.is_claimed,
            created_at=item_model.created_at,
            status=200,
            mssg="Success"
        )
    
class ItemList(BaseModel):
    item_list: List[ItemResponse]=[]
    count:int