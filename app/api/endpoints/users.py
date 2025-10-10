from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.models.user import *
from app.api.dependencies import get_current_user
from app.services.user_service import UserService
from app.api.dependencies import get_user_service



user_router= APIRouter()

@user_router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return current_user


@user_router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_update: UserCreation,
    service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
   
    updated_user = await service.update_user_profile(
        user_id=current_user.user_id,
        user_update=user_update
    )
    
    if not updated_user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found for update.")
         
    return updated_user