from typing import Dict, Optional, Annotated
from datetime import datetime
from app.models.user import UserCreation, UserResponse, UserModel 
from app.models.auth import LoginRequest, LoginResponse
from app.core import security
from app.repositories import user_repository
from fastapi import status, Depends

class AuthService:
    
    def __init__(self, user_repo:user_repository):
        self.user_repository = user_repo
        
    async def register_user(self, user_in:UserCreation) -> Optional[UserResponse]:
        
        existing_user_doc = await self.user_repository.get_user_by_id(user_in.user_id)
        if existing_user_doc:
            return UserResponse.from_model(
                UserModel(user_id=user_in.user_id, status=status.HTTP_400_BAD_REQUEST, mssg="Exists")
            )
            
        hashed_password = security.gen_pswd_hash(user_in.passwd)
        user_model = user_in.to_model(hashed_password=hashed_password, created_at=datetime.now())
        await self.user_repository.create_user(user_model)
        return UserResponse.from_model(user_model)
    
    async def verify_user(self, user_in:LoginRequest) -> Optional[LoginResponse]:
        
        user_doc = await self.user_repository.get_user_by_id(user_in.user_id)
        access_token = None
        if user_doc:
            # 1. Verify password using stored hash
            hashed_passwd = user_doc.get("hashed_password") # Retrieve hash from DB result
            is_correct = security.verify_pswd(user_in.passwd, hashed_passwd)
            
            if is_correct:
                # 2. Generate token on success
                access_token = security.create_access_token(user_data={"user_id": user_in.user_id})   
                ret_status = status.HTTP_200_OK
                mssg = "Login successful"
            else:
                status= status.HTTP_401_UNAUTHORIZED
                mssg= "Incorrect User ID or Password."
        
        return LoginResponse(
            user_id=user_in.user_id,
            status=ret_status,
            mssg=mssg,
            token=access_token
        )
           