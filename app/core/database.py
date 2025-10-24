

from motor.motor_asyncio import AsyncIOMotorClient
import os

# MongoDB connection settings
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "Lost_and_Found")

# Initialize the MongoDB client
client = AsyncIOMotorClient(MONGO_URI)

# Get the database instance
db = client[DB_NAME]

# Dependency for FastAPI (you’ll use this in your routes/services)
def get_db():
    return db
