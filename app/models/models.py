from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class user(BaseModel):
    reg_no: int  #offical reg no
    passwd: str  #passwd 
    acc_created: datetime  #day and time of reg
    email: Optional[str]=None #official email (optional)
    

    
    