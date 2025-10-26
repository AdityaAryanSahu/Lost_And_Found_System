from app.core.database import get_db
from app.models.auth import AuthSessionModel




class AuthRepo:
    
    async def create_session(self, session: AuthSessionModel):
        db=get_db()
        collection = db["sessions"]
        result = await collection.insert_one(session.to_dict())
        return str(result.inserted_id)

    async def get_session_by_user(self,user_id: str):
        db=get_db()
        collection = db["sessions"]
        return await collection.find_one({"user_id": user_id})

    async def delete_session(self,token: str):
        db=get_db()
        collection = db["sessions"]
        return await collection.delete_one({"token": token})
