from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# Global database instance
_db: AsyncIOMotorDatabase = None
_client: AsyncIOMotorClient = None

async def connect_to_mongo():
    """
    Connect to MongoDB when the application starts
    """
    global _db, _client
    try:
        logger.info(f"Connecting to MongoDB at {settings.MONGO_URI}")
        _client = AsyncIOMotorClient(settings.MONGO_URI)
        # Verify connection
        await _client.admin.command('ping')
        _db = _client[settings.DB_NAME]
        logger.info(f"✓ Connected to MongoDB successfully on database: {settings.DB_NAME}")
    except Exception as e:
        logger.error(f"✗ Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """
    Close MongoDB connection when the application stops
    """
    global _db, _client
    try:
        if _client:
            await _client.close()
            logger.info("✓ MongoDB connection closed")
    except Exception as e:
        logger.error(f"✗ Error closing MongoDB connection: {e}")

def get_db() -> AsyncIOMotorDatabase:
    """
    Get the database instance for use in services/routes
    """
    global _db
    if _db is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo() on startup.")
    return _db