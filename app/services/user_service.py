from typing import Optional, Dict, Annotated
from app.models.user import UserCreation,UserResponse, UserModel 
from app.repositories import user_repository
from fastapi import Depends


class UserService:
    def __init__(self, user_repo: user_repository):
        self.user_repository = user_repo
        
    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        
        user_doc = await self.user_repository.get_user_by_id(user_id)
        
        if user_doc:
            user_model = UserModel(**user_doc)
            return UserResponse.from_model(user_model)
            
        return None    
    
    async def update_user_profile(self, user_id: str, user_update: UserCreation) -> Optional[UserResponse]:
 
        update_data = user_update.model_dump(exclude_unset=True)
        
        await self.user_repository.update_user(user_id, update_data)
        

        return await self.get_user_by_id(user_id)