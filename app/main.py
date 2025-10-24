from fastapi import FastAPI,HTTPException
from app.api.router import api_router
from contextlib import asynccontextmanager
# from .database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Database initialization starting...")
   # create_db_and_tables() 
    print("Database and tables initialized successfully.")
    yield 
    print("Application shutdown complete.")
    
def create_app() -> FastAPI:
    app = FastAPI (
        title="Lost And Found Inventory",
        description="Backend for the Lost And Found Inventory",
        lifespan=lifespan
        )
    app.include_router(api_router)
    return app


app = create_app()