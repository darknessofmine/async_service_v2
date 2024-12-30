from typing import Annotated

from fastapi import APIRouter, Depends, Form, status

from .services import UserService
from api.auth.services import AuthService
from api.profiles.services import ProfileService
from api.users.schemas import UserResponse, UserUpdate
from core.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.patch("/me",
              response_model=UserResponse,
              status_code=status.HTTP_200_OK)
async def change_user_username_or_email(
    user_service: Annotated[UserService, Depends(UserService)],
    profile_service: Annotated[ProfileService, Depends(ProfileService)],
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    user_update: UserUpdate = Form(),
) -> UserResponse:
    user = await user_service.change_username_or_email(
        user=current_user,
        user_update=user_update,
    )
    await profile_service.change_profile_first_name_on_username_change(
        user=current_user,
        new_username=user_update.username,
    )
    return user
