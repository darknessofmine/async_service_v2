from typing import Annotated

from fastapi import APIRouter, Form, Depends, status

from .services import AuthService
from api.users.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserPasswordReset,
)
from api.auth.access_token.schemas import TokenInfo
from api.profiles.services import ProfileService
from background_tasks import tasks
from core.models import User
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
    profile_service: Annotated[ProfileService, Depends(ProfileService)],
    user_create: UserCreate,
) -> UserResponse:
    user = await auth_service.create_user(user_create)
    await profile_service.create_user_profile(user)
    return user


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
    return {"message": "Password has been changed!"}


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    auth_service: Annotated[AuthService, Depends(AuthService)],
    username: str,
) -> dict[str, str]:
    user = await auth_service.get_user_by_username(username)
    reset_token = auth_service.get_reset_token_for_user(user)
    tasks.send_reset_token.delay(user.email, reset_token)
    return {"message": "Your reset token has been sent to you by email."}


@router.post("/reset-password")
async def reset_password(
    auth_service: Annotated[AuthService, Depends(AuthService)],
    reset_user: Annotated[User, Depends(AuthService.get_user_by_reset_token)],
    new_password: UserPasswordReset = Form(),
) -> dict[str, str]:
    await auth_service.reset_user_password(reset_user, new_password)
    return {"message": "Password has been changed!"}


@router.post("/verificaion", status_code=status.HTTP_200_OK)
async def send_verification_email(
    auth_service: Annotated[AuthService, Depends(AuthService)],
    current_user: Annotated["User", Depends(AuthService.get_current_user)],
) -> dict[str, str]:
    url = auth_service.create_verification_url(current_user)
    tasks.send_verification_url.delay(current_user.email, url)
    return {
        "message": (
            "Verification message has been sent to you! "
            "Please check your email."
        )
    }


@router.get("/verification/{token}", status_code=status.HTTP_200_OK)
async def verify_user(
    auth_service: Annotated[AuthService, Depends(AuthService)],
    token: str,
) -> dict[str, str]:
    await auth_service.verify_user_by_token(token)
    return {"message": "Your account has been verified!"}


@router.get("/me",
            response_model=UserResponse,
            status_code=status.HTTP_200_OK)
async def me(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
) -> UserResponse:
    return current_user
