from fastapi import APIRouter
from .endpoints import auth, items, users, claims, matches, search, messages

api_router = APIRouter()

#include routers for all as you gp on
api_router.include_router(auth.auth_router, tags=["Authentication"], prefix="/auth")
api_router.include_router(items.item_router, tags=["Items"], prefix="/items")
api_router.include_router(users.user_router, tags=["Users"], prefix="/users")
api_router.include_router(claims.claim_router, tags=["Claims"], prefix="/claims")
api_router.include_router(matches.match_router, tags=["Matches"], prefix="/matches")
api_router.include_router(search.search_router, tags=["Search"], prefix="/search")
api_router.include_router(messages.router)