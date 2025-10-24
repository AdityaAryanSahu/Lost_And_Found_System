from app.core.database import db
from app.models.auth import AuthSessionModel

collection = db["sessions"]

class AuthRepo:
    
    async def create_session(session: AuthSessionModel):
        result = await collection.insert_one(session.to_dict())
        return str(result.inserted_id)

    async def get_session_by_user(user_id: str):
        return await collection.find_one({"user_id": user_id})

    async def delete_session(token: str):
        return await collection.delete_one({"token": token})
