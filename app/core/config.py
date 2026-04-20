from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Lost and Found"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database - MongoDB
    MONGO_URI: str = os.getenv(
        "MONGO_URI"
    )
    DB_NAME: str = os.getenv("DB_NAME")
    
    # JWT/Security
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    
    # R2 Storage (for both dev and production)
    R2_ENDPOINT: str = os.getenv("R2_ENDPOINT")
    R2_ACCESS_KEY: str = os.getenv("R2_ACCESS_KEY")
    R2_SECRET_KEY: str = os.getenv("R2_SECRET_KEY")
    R2_BUCKET_NAME: str = os.getenv("R2_BUCKET_NAME")
    R2_PUBLIC_URL: str = os.getenv("R2_PUBLIC_URL")
    
    class Config:
        env_file = ".env"

settings = Settings()