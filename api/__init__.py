__all__ = (
    "api_router",
)


from fastapi import APIRouter

from .auth.routes import router as auth_router
from .comments.routes import router as comment_router
from .follows. routes import router as follow_router
from .posts.routes import router as post_router
from .profiles.routes import router as profile_router
from .sub_tiers.routes import router as sub_tier_router
from .subscriptions.routes import router as subscription_router
from .users.routes import router as user_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(profile_router)
api_router.include_router(sub_tier_router)
api_router.include_router(post_router)
api_router.include_router(comment_router)
api_router.include_router(subscription_router)
api_router.include_router(follow_router)
