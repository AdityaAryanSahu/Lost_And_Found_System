from app.core.database import get_db
from app.models.claim import ClaimModel



class ClaimRepo:
    
    async def create_claim(self,claim: ClaimModel):
        db=get_db()
        collection = db["claims"]   
        result = await collection.insert_one(claim.to_dict())
        return str(result.inserted_id)

    async def get_claim_by_id(self,claim_id: str):
        db=get_db()
        collection = db["claims"]
        return await collection.find_one({"claim_id": claim_id})

    async def get_claims_for_item(self,item_id: str, limit: int = 20):
        db=get_db()
        collection = db["claims"]
        return await collection.find({"item_id": item_id}).to_list(length=limit)

    async def update_claim_status(self,claim_id: str, status: str):
        db=get_db()
        collection = db["claims"]
        return await collection.update_one({"claim_id": claim_id}, {"$set": {"status": status}})

    async def delete_claim(self,claim_id: str):
        db=get_db()
        collection = db["claims"]
        return await collection.delete_one({"claim_id": claim_id})
    
    async def update_claim_fields(self,claim_id: str, update_data: dict):
        db=get_db()
        collection = db["claims"]
        return await collection.update_one(
        {"claim_id": claim_id},
        {"$set": update_data}
    )
