from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    user_id:str
    passwd:str
    email:Optional[str]=None

class LoginResponse(BaseModel):
    user_id:str 
    status:int
    mssg:str
    token: Optional[str] = None
    