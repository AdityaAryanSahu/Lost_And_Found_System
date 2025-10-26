from pydantic import BaseModel, Field,ConfigDict
from typing import Optional
from datetime import datetime

class AuthSessionModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[str] = Field(None, alias="_id")
    user_id: str                                
    token: str
    expires_at: datetime
    
    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)
    
class LoginRequest(BaseModel):
    user_id:str
    passwd:str
    email:Optional[str]=None

class LoginResponse(BaseModel):
    user_id:str 
    status:int
    mssg:str
    token: Optional[str] = None
    