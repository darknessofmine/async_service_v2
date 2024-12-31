from typing import Annotated

from fastapi import APIRouter, Depends, Form, status

from .services import UserService
from api.auth.permissions import Permissions
from api.auth.services import AuthService
from api.profiles.services import ProfileService
from api.users.schemas import UserCreate, UserResponse, UserUpdate
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
    updated_user = await user_service.change_username_or_email(
        user=current_user,
        user_update=user_update,
    )
    await profile_service.change_profile_name_on_username_change(
        user=current_user,
        new_username=user_update.username,
    )
    return updated_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_service: Annotated[UserService, Depends(UserService)],
    current_suer: Annotated[User, Depends(AuthService.get_current_user)],
) -> None:
    await user_service.delete_user(current_suer)


@router.post("/create-superuser",
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
async def create_superuser(
    user_service: Annotated[UserService, Depends(UserService)],
    current_user: Annotated[bool, Depends(Permissions(["is_admin"]))],
    superuser: UserCreate,
) -> UserResponse:
    return await user_service.create_superuser(user=superuser)
