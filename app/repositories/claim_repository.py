from app.core.database import db
from app.models.claim import ClaimModel

collection = db["claims"]

class ClaimRepo:
    
    async def create_claim(claim: ClaimModel):
        result = await collection.insert_one(claim.to_dict())
        return str(result.inserted_id)

    async def get_claim_by_id(claim_id: str):
        return await collection.find_one({"claim_id": claim_id})

    async def get_claims_for_item(item_id: str, limit: int = 20):
        return await collection.find({"item_id": item_id}).to_list(length=limit)

    async def update_claim_status(claim_id: str, status: str):
        return await collection.update_one({"claim_id": claim_id}, {"$set": {"status": status}})

    async def delete_claim(claim_id: str):
        return await collection.delete_one({"claim_id": claim_id})
    
    async def update_claim_fields(claim_id: str, update_data: dict):
        return await collection.update_one(
        {"claim_id": claim_id},
        {"$set": update_data}
    )
