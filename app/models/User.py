from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UserCreation(BaseModel):
    reg_no: int  #offical reg no
    passwd: str  #passwd 
    email: Optional[str]=None #official email (optional)
    
class UserResponse(BaseModel):
    reg_no:int
    email: Optional[str]=None
    acc_created: datetime
    mssg:str
    
    

    
    