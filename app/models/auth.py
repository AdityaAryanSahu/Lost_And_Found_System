from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    reg_no:int
    passwd:str
    email:Optional[str]=None

class LoginResponse(BaseModel):
    reg_no:int
    status:int
    mssg:str
    