from typing import Dict, Optional
from datetime import datetime
from app.models.user import UserCreation, UserResponse
from app.models.auth import LoginRequest, LoginResponse
from app.core import security
from fastapi import status, HTTPException

class AuthService:
    async def register_user(self, user_in:UserCreation) -> Optional[UserResponse]:
        
        #first check if user alreadt exists
        
        hashed_password = security.gen_pswd_hash(user_in.passwd)
        user_response = UserResponse(
            user_id=user_in.user_id,
            email=user_in.email,
            acc_created=datetime.now(),
            status=status.HTTP_201_CREATED,
            mssg="User registered successfully."
        )
        
        #push the data in database

        return user_response
    
    async def verify_user(self, user_in:LoginRequest) -> Optional[LoginResponse]:
        
        #get user details from database on basis of user_in.user_id
        #hashed_passwd= (get from database)
        
        is_correct = security.verify_pswd(user_in.passwd, hashed_passwd)
        if is_correct == True:
            access_token = security.create_access_token(
                data={"user_id": user_in.user_id}
                )   
            status= status.HTTP_200_OK
            mssg= "Login succesful"
        else:
            status= status.HTTP_401_UNAUTHORIZED
            mssg= "Incorrect User ID or Password."
        
        ret_resp=LoginResponse(
            user_id=user_in.user_id,
            status=status,
            mssg=mssg,
            token=access_token
        )
        return ret_resp
           