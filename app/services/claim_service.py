from typing import Optional, List
from datetime import datetime
from app.models.claim import ClaimCreation, ClaimResponse
from app.services.item_service import ItemService
import uuid


class ClaimService:
    def __init__(self):
        self.item_serv=ItemService()
        
    async def claim_submit(self, claim_data: ClaimCreation, user_id: str) -> Optional[ClaimResponse]:
        
        item=await self.item_serv.get_item_id(claim_data.item_id)
        
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
        claim_res=ClaimResponse(
            item_id=claim_data.item_id, user_id=user_id, claim_id=new_claim_id,
                 mssg="Successfully submitted", status="PENDING",
                 submitted_at=datetime.now()
        )
        
        #store in database
        
        return claim_res
    
    async def get_claims_item_id(self, item_id:str) -> List[ClaimResponse]:
        #get all claims for item_id and create a response body for each
        #pu them in a list and return them
        return List[]
    
    async def review_claim(self, claim_id: str, current_user_id: int, action: str) -> ClaimResponse:
        
        #get the claim data and make a claim body
        #claim=db.get(claim_id)
        
        if not claim:
            return ClaimResponse(
               claim_id=claim_id, item_id="", user_id=current_user_id,
                status="FAILED", mssg="Claim not found"
            )
        item = await self.item_serv.get_item_id(claim.item_id)
        if not item or item.user_id != current_user_id:
            return ClaimResponse(
                claim_id=claim_id, item_id=claim.item_id, user_id=current_user_id,
                status="FAILED", mssg="Not authorized to manage this claim."
            )
        if claim.status != "PENDING":
             return ClaimResponse(
                claim_id=claim_id, item_id=claim.item_id, user_id=current_user_id,
                status="FAILED", mssg=f"Claim is already {claim.status}."
            )
            
        if action.upper() == "APPROVE":
            await self.item_service.mark_item_claimed(claim.item_id)
            claim.status = "APPROVED"
            claim.mssg = "Claim approved and item marked as claimed."
            
        elif action.upper() == "REJECT":
            claim.status = "REJECTED"
            claim.mssg = "Claim rejected."
            
        else:
            return ClaimResponse(
                claim_id=claim_id, item_id=claim.item_id, user_id=current_user_id,
                status="FAILED", mssg="Invalid action."
            )
            
        return claim
    
    
        