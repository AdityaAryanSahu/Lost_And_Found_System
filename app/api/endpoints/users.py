from fastapi import FastAPI, APIRouter, Depends
from typing import Annotated
from app.models.user import *
from app.api.dependencies import get_current_user



user_router= APIRouter()

@user_router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return current_user