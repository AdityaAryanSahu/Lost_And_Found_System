from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from typing import Optional, Annotated, List
from app.models.claim import ClaimCreation, ClaimResponse
from app.models.user import UserCreation, UserResponse
from app.services.claim_service import ClaimService
from app.api.dependencies import get_claim_service, get_current_user


claim_router=FastAPI()

@claim_router.post("/", response_model=ClaimResponse)
async def submit_claim(
    claim_data: ClaimCreation, service: Annotated[ClaimService, Depends(get_claim_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    claim_res = await service.submit_claim(
        claim_data=claim_data, 
        user_id=current_user.user_id
    )
    
    if claim_res.status == "Failed":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=claim_res.mssg
        )
        
    return claim_res

@claim_router.get("/item/{item_id}", response_model=List[ClaimResponse])
async def all_claims( item_id: str,
    service: Annotated[ClaimService, Depends(get_claim_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)]):
    
    claims = await service.get_claims_item_id(item_id)
    return claims

@claim_router.post("/{claim_id}/review/{action}", response_model=ClaimResponse)
async def claim_review(
    claim_id: str,
    action: str,
    service: Annotated[ClaimService, Depends(get_claim_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)]
    ):
    
    claim = await service.review_claim(claim_id, current_user.user_id, action)
    if claim.status == "FAILED":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=claim.mssg)
    return claim

