from app.core import security
from fastapi import Depends, HTTPException, status
from app.models.user import UserResponse
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Optional
from app.services.auth_service import AuthService
from app.services.item_service import ItemService
from app.services.match_service import MatchService
from app.services.claim_service import ClaimService
from app.services.image_service import ImageService
from app.services.user_service import UserService
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



def get_auth_service():
    return AuthService()

def get_item_service():
    return ItemService()

def get_claim_service():
    return ClaimService()

def get_match_service():
    return MatchService()

def get_image_service():
    return ImageService()

def get_user_service():
    return UserService()

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserResponse:
    
    # Decodes the JWT token from the 'Bearer' header and returns the authenticated UserResponse.
    
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
  
        token_data = security.decode_token(token) 
    
        if token_data is None:
            raise credentials_exception

        user_id: int = token_data.get("sub") 
    
        if user_id is None:
            raise credentials_exception

    # get user data from db: user_entry = db.get(user_id)
    
        if user_entry is None:
            raise credentials_exception
    
        return user_entry["data"] 

