from typing import Dict, Optional, Annotated
from datetime import datetime
from app.models.user import UserCreation, UserResponse, UserModel 
from app.models.auth import LoginRequest, LoginResponse
from app.core import security
from app.repositories import user_repository
from fastapi import status, Depends, HTTPException

class AuthService:
    
    def __init__(self, user_repo: user_repository):
        self.user_repository = user_repo
        
    async def register_user(self, user_in:UserCreation) -> Optional[UserResponse]:
        
        existing_user_doc = await self.user_repository.get_user_by_id(user_in.user_id)
        if existing_user_doc:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
            
        hashed_password = security.gen_pswd_hash(user_in.passwd)
        user_model = user_in.to_model(hashed_password=hashed_password, created_at=datetime.now())
        await self.user_repository.create_user(user_model)
        return UserResponse.from_model(user_model)
    
    async def verify_user(self, user_in: LoginRequest) -> Optional[LoginResponse]:
        ret_status = None
        mssg = "User not found"
        access_token = None
        
        user_doc = await self.user_repository.get_user_by_id(user_in.user_id)
        
        if user_doc:
            hashed_passwd = user_doc.get("hashed_password")
            is_correct = security.verify_pswd(user_in.passwd, hashed_passwd)
            
            if is_correct:
                access_token = security.create_access_token({"user_id": user_in.user_id})
                ret_status = status.HTTP_200_OK
                mssg = "Login successful"
            else:
                ret_status = status.HTTP_401_UNAUTHORIZED
                mssg = "Incorrect password"
        else:
            ret_status = status.HTTP_404_NOT_FOUND
        
        return LoginResponse(
            user_id=user_in.user_id,
            status=ret_status,
            mssg=mssg,
            token=access_token
        )
           