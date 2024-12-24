from typing import Annotated

from fastapi import APIRouter, Form, Depends, status

from .services import AuthService, UserValidationService
from api.users.schemas import UserCreate, UserLogin, UserResponse
from api.auth.access_token.schemas import AccessTokenInfo
from core.settings import settings


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(settings.auth.transport)],
)


@router.post("/signup",
             response_model=UserResponse,
             status_code=status.HTTP_200_OK)
async def signup(
    auth_service: Annotated[AuthService, Depends(AuthService)],
    user_create: UserCreate,
) -> UserResponse:
    return await auth_service.create_user(user_create)


@router.post("/login",
             response_model=AccessTokenInfo,
             status_code=status.HTTP_200_OK)
async def login(
    auth_service: Annotated[AuthService, Depends(AuthService)],
    user: UserLogin = Form(),
) -> AccessTokenInfo:
    return await auth_service.get_access_token_for_user(user)


@router.get("/me",
            response_model=UserResponse,
            status_code=status.HTTP_200_OK)
async def me(
    validation_service: Annotated[
        UserValidationService,
        Depends(UserValidationService),
    ],
) -> UserResponse:
    return await validation_service.get_current_user()
