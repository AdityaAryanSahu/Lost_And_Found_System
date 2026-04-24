from typing import Dict, Optional, Annotated
from datetime import datetime, timedelta
from app.models.user import UserCreation, UserResponse, UserModel 
from app.models.auth import LoginRequest, LoginResponse, AuthSessionModel
from app.core import security
from app.repositories.auth_repository import AuthRepo
from  app.repositories.user_repository import UserRepo
from fastapi import status, Depends, HTTPException

class AuthService:
    
    def __init__(self, user_repo: UserRepo, auth_repo: AuthRepo):
        self.user_repository = user_repo
        self.auth_repository= auth_repo
        
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
        refresh_token= None
        expires_at = timedelta(days=30)
        user_doc = await self.user_repository.get_user_by_id(user_in.user_id)
        
        if user_doc:
            hashed_passwd = user_doc.get("hashed_password")
            is_correct = security.verify_pswd(user_in.passwd, hashed_passwd)
            
            if is_correct:
                access_token = security.create_access_token({"user_id": user_in.user_id})
                refresh_token = security.create_access_token({"user_id": user_in.user_id}, expiry=expires_at, refresh=True)
                await self.auth_repository.create_session(
                    AuthSessionModel(
                        user_id=user_in.user_id,
                        token=refresh_token,
                        expires_at=datetime.utcnow() + expires_at
                    )
                )
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
            access_token=access_token, 
            refresh_token=refresh_token
        )
        
    async def refresh_access_token(self, refresh_token: str) -> str :
        token_data = security.decode_token(refresh_token)
        
        if not token_data:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not a refresh token")
        
        user_id= token_data.get("sub")
        
        session = await self.auth_repository.get_session_by_user(user_id)
        if not session or session["expires_at"] < datetime.utcnow():
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Refresh token expired")
        
        return security.create_access_token({"user_id": user_id})
    
        
           