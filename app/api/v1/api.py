from fastapi import APIRouter

from app.api.v1.endpoints import auth, movies, search, users

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(movies.router, prefix="/movies", tags=["Movies"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
