from typing import Optional
from app.models.user import UserResponse, UserCreation


class UserService:
    
    async def update_user_profile(self, user_id: str, user_update: UserCreation) -> Optional[UserResponse]:

        
       # get data of user and create user response body: user_entry = db.get(user_id)
        if not user_entry:
            return None
        
        existing_user: UserResponse = user_entry["data"]
        
        update_data = user_update.model_dump(exclude_unset=True)
        
        if 'email' in update_data:
            existing_user.email = update_data['email']
        

        return existing_user