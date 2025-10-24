from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class UserModel(BaseModel):
    # MongoDB ObjectId field
    id: Optional[str] = Field(None, alias="_id") 
    
    user_id: str                           
    username: str
    email: Optional[str] = None
    hashed_password: str                    
    acc_created: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)
    
class UserCreation(BaseModel):
    username:str
    user_id: str  #offical reg no
    passwd: str  #passwd 
    email: Optional[str]=None #official email (optional)
    def to_model(self, hashed_password: str, created_at: datetime) -> UserModel:
        return UserModel(
            user_id=self.user_id,
            username=self.username,
            email=self.email,
            hashed_password=hashed_password,
            acc_created=created_at
        )
    
class UserResponse(BaseModel):
    user_id:str
    email: Optional[str]=None
    acc_created: datetime
    status:int
    mssg:str
    @classmethod
    def from_model(cls, user_model: UserModel) -> 'UserResponse':
        return cls(
            user_id=user_model.user_id,
            email=user_model.email,
            acc_created=user_model.acc_created,
            status=200, 
            mssg="Success"
        )
    
    

    
    