from app.core.database import get_db
from app.models.user import UserModel


class UserRepo:
    async def create_user(self,user: UserModel):
        db=get_db()
        collection = db["users"]
        result = await collection.insert_one(user.to_dict())
        return str(result.inserted_id)

    async def get_user_by_id(self,user_id: str):
        db=get_db()
        collection = db["users"]
        return await collection.find_one({"user_id": user_id})

    async def get_user_by_email(self,email: str):
        db=get_db()
        collection = db["users"]
        return await collection.find_one({"email": email})

    async def get_all_users(self,limit: int = 100, offset: int = 0):
        db=get_db()
        collection = db["users"]
        return await collection.find().skip(offset).limit(limit).to_list(length=limit)

    async def delete_user(self,user_id: str):
        db=get_db()
        collection = db["users"]
        return await collection.delete_one({"user_id": user_id})
