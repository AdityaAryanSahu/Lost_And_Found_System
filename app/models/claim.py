from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any, Dict

class ClaimModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    
    claim_id: str
    item_id: str
    user_id: str                                
    justification: str
    status: str = "PENDING"
    submitted_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)
    
class ClaimCreation(BaseModel):
    item_id:str
    user_id:str
    justification: str
    def to_model(self, claim_id: str, submitted_at: datetime) -> ClaimModel:
        return ClaimModel(
            claim_id=claim_id,
            item_id=self.item_id,
            user_id=self.user_id,
            justification=self.justification,
            submitted_at=submitted_at
        )
    
class ClaimResponse(BaseModel):
    item_id:str
    user_id:str
    claim_id:str
    mssg:str
    status:str
    submitted_at: datetime
    @classmethod
    def from_model(cls, claim_model: ClaimModel) -> 'ClaimResponse':
        return cls(
            item_id=claim_model.item_id,
            user_id=claim_model.user_id,
            claim_id=claim_model.claim_id,
            mssg="Claim data retrieved",
            status=claim_model.status,
            submitted_at=claim_model.submitted_at
        )