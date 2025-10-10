from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from typing import Optional, Annotated
from app.models.auth import LoginRequest, LoginResponse
from app.models.user import UserCreation, UserResponse
from app.services.auth_service import AuthService
from app.api.dependencies import get_auth_service

auth_router = APIRouter()



@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreation, service: Annotated[AuthService, Depends(get_auth_service)]):
    new_user = await service.register_user(user_in)
    if new_user.status != status.HTTP_201_CREATED:
        raise HTTPException(status_code=new_user.status,detail=new_user.mssg)
    return new_user

@auth_router.post("/login", response_model=LoginResponse)
async def login(user_in:LoginRequest, service= Annotated[AuthService, Depends(get_auth_service)]):
    verification = await service.verify_user(user_in)
    if verification.status != status.HTTP_200_OK :
        raise HTTPException(status_code=verification.status, detail=verification.mssg)
    return verification