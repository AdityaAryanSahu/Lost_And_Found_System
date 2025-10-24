from typing import Optional, List, Annotated, Dict
from datetime import datetime
from app.models.claim import ClaimCreation, ClaimResponse, ClaimModel 
from app.models.user import UserResponse, UserModel
from app.services.item_service import ItemService
from app.services.noti_service import NotificationService 
from app.repositories import user_repository, claim_repository
from fastapi import Depends, HTTPException, status
import uuid


class ClaimService:
    def __init__(self,
                 item_service: Annotated[ItemService, Depends()],
                 noti_service: Annotated[NotificationService, Depends()],
                 claim_repo: claim_repository,
                 user_repo: user_repository): # For fetching claimant data
        self.item_service = item_service
        self.notification_service = noti_service
        self.claim_repository = claim_repo
        self.user_repository = user_repo
        
    async def claim_submit(self, claim_data: ClaimCreation, user_id: str) -> Optional[ClaimResponse]:
        
        item=await self.item_service.get_item_id(claim_data.item_id)
        
        if item is None:
            return ClaimResponse(
                 item_id=claim_data.item_id, user_id=user_id, claim_id="N/A",
                 mssg="Item not found.", status="Failed",
                 submitted_at=datetime.now()
            )
        
        if item.is_claimed:
            return ClaimResponse(
                 item_id=claim_data.item_id, user_id=user_id, claim_id="N/A",
                 mssg="Item Already claimed", status="Failed",
                 submitted_at=datetime.now()
            )
        
        new_claim_id = str(uuid.uuid4())
        claim_model = claim_data.to_model(claim_id=new_claim_id, submitted_at=datetime.now())
        claim_model.user_id = user_id
        await self.claim_repository.create_claim(claim_model)
        claimant_doc = await self.user_repository.get_user_by_id(user_id)
        if claimant_doc:
             claimant = UserResponse.from_model(UserModel(**claimant_doc))
             await self.notification_service.notify_item_poster_of_claim(item=item, claimant=claimant)
      
        return ClaimResponse.from_model(claim_model)
    
    async def get_claims_item_id(self, item_id:str) -> List[ClaimResponse]:
        claim_docs = await self.claim_repository.get_claims_for_item(item_id)
        claims = [ClaimResponse.from_model(ClaimModel(**doc)) for doc in claim_docs]
        return claims
    
    async def review_claim(self, claim_id: str, current_user_id: str, action: str) -> ClaimResponse:
        
        claim_doc = await self.claim_repository.get_claim_by_id(claim_id)
        
        if not claim_doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found.")
            
        claim_model = ClaimModel(**claim_doc)
        item_res = await self.item_service.get_item_id(claim_model.item_id)
        if not item_res or item_res.user_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to review this claim.")
            
       
        if claim_model.status != "PENDING":
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Claim is already {claim_model.status}.")
            
    
        action = action.upper()
        if action not in ["APPROVE", "REJECT"]:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid action.")
            
        update_data = {"status": action, "mssg": f"Claim {action.lower()}."}
        
        if action == "APPROVE":
            await self.item_service.mark_item_claimed(claim_model.item_id)
            
       
        await self.claim_repository.update_claim_fields(claim_id, update_data)
        
        
        claimant_doc = await self.user_repository.get_user_by_id(claim_model.user_id)
        if claimant_doc:
            claimant = UserResponse.from_model(UserModel(**claimant_doc))
            await self.notification_service.notify_claimant_of_decision(claimant, item_res, action)
            
    
        return await self.get_claim_by_id(claim_id)
    
    
        