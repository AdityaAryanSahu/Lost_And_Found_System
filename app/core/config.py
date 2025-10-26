from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Lost and Found"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database - MongoDB
    MONGO_URI: str = os.getenv(
        "MONGO_URI", 
        "mongodb://localhost:27017/"
    )
    DB_NAME: str = os.getenv("DB_NAME", "Lost_and_Found")
    
    # JWT/Security
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "b6718f5b621697e4b10ed7c6187bca24")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # MinIO Storage (for both dev and production)
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ROOT_USER: str = os.getenv("MINIO_ROOT_USER", "minio_user")
    MINIO_ROOT_PASSWORD: str = os.getenv("MINIO_ROOT_PASSWORD", "minio_password")
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "False").lower() == "true"
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", "lost-and-found")
    
    class Config:
        env_file = ".env"

settings = Settings()