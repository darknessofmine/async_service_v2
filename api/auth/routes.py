from typing import Annotated

from fastapi import APIRouter, Form, Depends, status

from .services import AuthService
from api.users.schemas import UserCreate, UserLogin, UserResponse
from api.auth.access_token.schemas import TokenInfo
from core.settings import settings
from core.models import User


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
             response_model=TokenInfo,
             status_code=status.HTTP_200_OK)
async def login(
    auth_service: Annotated[AuthService, Depends(AuthService)],
    user: UserLogin = Form(),
) -> TokenInfo:
    tokens = await auth_service.get_access_and_refresh_tokens_for_user(user)
    return TokenInfo(**tokens)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    auth_service: Annotated[AuthService, Depends(AuthService)],
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
) -> dict[str, str]:
    await auth_service.delete_refresh_token(current_user)
    return {"message": "You've successfully logged out."}


@router.put("/change-password", status_code=status.HTTP_201_CREATED)
async def change_password(
    auth_service: Annotated[AuthService, Depends(AuthService)],
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    old_password: str,
    new_password: str,
) -> dict[str, str]:
    await auth_service.change_user_password(
        current_user,
        new_password=new_password,
        old_password=old_password,
    )
    return {"message": "Password successfully changed!"}


@router.post("/forgot-password", status_code=status.HTTP_201_CREATED)
async def forgot_password(
    auth_service: Annotated[AuthService, Depends(AuthService)],
):
    ...


@router.post("/")
async def reset_password():
    ...


@router.get("/me",
            response_model=UserResponse,
            status_code=status.HTTP_200_OK)
async def me(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
) -> UserResponse:
    return current_user
