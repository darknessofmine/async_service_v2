from typing import Annotated

from fastapi import APIRouter, Depends, Form, status

from .schemas import ProfileResponse, ProfileUpdate
from .services import ProfileService
from api.auth.services import AuthService
from core.models import User


router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)


@router.get("/{username}",
            response_model=ProfileResponse,
            status_code=status.HTTP_200_OK)
async def get_user_profile(
    profile_service: Annotated[ProfileService, Depends(ProfileService)],
    username: str,
) -> ProfileResponse:
    return await profile_service.get_user_profile_by_username(username)


@router.patch("/update",
              response_model=ProfileResponse,
              status_code=status.HTTP_200_OK)
async def update_profile(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    profile_service: Annotated[ProfileService, Depends(ProfileService)],
    profile_update: ProfileUpdate = Form(),
) -> ProfileResponse:
    return await profile_service.update_user_profile(
        user=current_user,
        profile_update=profile_update,
    )
