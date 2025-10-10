from pydantic import BaseModel
from datetime import datetime

class ClaimCreation(BaseModel):
    item_id:str
    user_id:str
    justification: str
    
class ClaimResponse(BaseModel):
    item_id:str
    user_id:str
    claim_id:str
    mssg:str
    status:str
    submitted_at: datetime