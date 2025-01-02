from typing import Annotated

from fastapi import APIRouter, Depends, status

from .services import UserService
from api.auth.permissions import Permissions
from api.auth.services import AuthService
from api.users.schemas import UserCreate, UserResponse, UserUpdate
from core.models import User


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.patch("/me",
              response_model=UserResponse,
              status_code=status.HTTP_200_OK)
async def change_user_email(
    user_service: Annotated[UserService, Depends(UserService)],
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    user_update: UserUpdate,
) -> UserResponse:
    updated_user = await user_service.change_user_email(
        user=current_user,
        user_update=user_update,
    )
    return updated_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_service: Annotated[UserService, Depends(UserService)],
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
) -> None:
    await user_service.delete_user(current_user)


@router.post(
    "/create-superuser",
    response_model=UserResponse,
    dependencies=[Depends(Permissions(["is_admin"]))],
    status_code=status.HTTP_201_CREATED)
async def create_superuser(
    user_service: Annotated[UserService, Depends(UserService)],
    superuser: UserCreate,
) -> UserResponse:
    return await user_service.create_superuser(user=superuser)
