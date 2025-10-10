from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UserCreation(BaseModel):
    username:str
    user_id: str  #offical reg no
    passwd: str  #passwd 
    email: Optional[str]=None #official email (optional)
    
class UserResponse(BaseModel):
    user_id:str
    email: Optional[str]=None
    acc_created: datetime
    status:int
    mssg:str
    
    

    
    