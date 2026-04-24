from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from typing import Optional, Annotated
from app.models.auth import LoginRequest, LoginResponse
from app.models.user import UserCreation, UserResponse
from app.services.auth_service import AuthService
from app.api.dependencies import get_auth_service
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter()



@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreation, service: Annotated[AuthService, Depends(get_auth_service)]):
    new_user = await service.register_user(user_in)
    if new_user.status != status.HTTP_201_CREATED:
        raise HTTPException(status_code=new_user.status,detail=new_user.mssg)
    return new_user

@auth_router.post("/login", response_model=LoginResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: Annotated[AuthService, Depends(get_auth_service)]):
    user_in = LoginRequest(
        user_id=form_data.username,
        passwd=form_data.password
    )
    
    verification = await service.verify_user(user_in)
    if verification.status != status.HTTP_200_OK :
        raise HTTPException(status_code=verification.status, detail=verification.mssg)
    return verification

@auth_router.post("/refresh")
async def refresh_token(refresh_token:str, service: Annotated[AuthService, Depends(get_auth_service)]):
    new_access_token= await service.refresh_access_token(refresh_token)
    return {"access_token": new_access_token}