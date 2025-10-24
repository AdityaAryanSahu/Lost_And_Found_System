from app.core.database import db
from app.models.user import UserModel

collection = db["users"]
class UserRepo:
    async def create_user(user: UserModel):
        result = await collection.insert_one(user.to_dict())
        return str(result.inserted_id)

    async def get_user_by_id(user_id: str):
        return await collection.find_one({"user_id": user_id})

    async def get_user_by_email(email: str):
        return await collection.find_one({"email": email})

    async def get_all_users(limit: int = 100, offset: int = 0):
        return await collection.find().skip(offset).limit(limit).to_list(length=limit)

    async def delete_user(user_id: str):
        return await collection.delete_one({"user_id": user_id})
