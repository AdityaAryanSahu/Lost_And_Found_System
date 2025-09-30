from pydantic import BaseModel


class ClaimCreation(BaseModel):
    item_id:int
    user_id:int
    
class ClaimResponse(BaseModel):
    item_id:int
    user_id:int
    claim_id:int
    mssg:str
    status:str