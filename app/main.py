from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api.router import api_router
from app.core.database import connect_to_mongo, close_mongo_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
   
    #Startup
    print("=" * 50)
    print("Database initialization starting...")
    try:
        await connect_to_mongo()
        print("Database and MongoDB connected successfully.")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise
    print("=" * 50)
    
    yield  
    
    #Shutdown
    print("=" * 50)
    print("Application shutdown starting...")
    try:
        await close_mongo_connection()
        print("Application shutdown complete.")
    except Exception as e:
        print(f"Error during shutdown: {e}")
    print("=" * 50)


def create_app() -> FastAPI:
   
    app = FastAPI(
        title="Lost And Found Inventory",
        description="Backend for the Lost And Found Inventory System",
        version="1.0.0",
        lifespan=lifespan
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
        "http://localhost:3000",      
        "http://127.0.0.1:3000",      
        ],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(api_router)
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": "Lost and Found API"
        }
    
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)