__all__ = (
    "api_router",
)


from fastapi import APIRouter

from .auth.routes import router as auth_router
from .profiles.routes import router as profile_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(profile_router)
