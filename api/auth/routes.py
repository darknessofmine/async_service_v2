from typing import Annotated

from fastapi import APIRouter, Depends, status

# from .dependencies import get_auth_service
from .service import AuthService
from api.users.schemas import UserCreate, UserLogin, UserResponse
from api.auth.access_token.schemas import AccessTokenInfo


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup",
             response_model=UserResponse,
             status_code=status.HTTP_200_OK)
async def signup(
    user_create: UserCreate,
    auth_service: Annotated[AuthService, Depends(AuthService)],
) -> UserResponse:
    return await auth_service.create_user(user_create)


@router.post("/login",
             response_model=AccessTokenInfo,
             status_code=status.HTTP_200_OK)
async def login(
    user: UserLogin,
    auth_service: Annotated[AuthService, Depends(AuthService)],
) -> AccessTokenInfo:
    validated_user = await auth_service.validate_auth_user(user)
    return await auth_service.create_access_token(user_id=validated_user.id)
