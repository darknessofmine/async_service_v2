from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from .repositories import UserRepo
from .schemas import UserCreate, UserUpdate
from api.auth import utils as auth_utils


if TYPE_CHECKING:
    from core.models import User


class UserService:
    def __init__(
        self,
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
    ) -> None:
        self.user_repo: UserRepo = user_repo

    async def create_superuser(self, user: UserCreate) -> "User":
        """
        Create new superuser.

        Raise `http_400_bad_request` exception if user with provided
        `username` or `email` already exists.
        """
        user_dict = {
            "username": user.username,
            "password": auth_utils.hash_password(user.password),
            "email": user.email,
            "is_verified": True,
            "is_admin": True,
            "is_superuser": True,
        }
        try:
            return await self.user_repo.create(user_dict)
        except IntegrityError as error:
            orig_detail = error.__dict__["orig"]
            error_field = str(orig_detail).split("\"")[3]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with {error_field} already exists!",
            )

    async def change_author_status(
        self,
        user: "User",
        author_status: bool,
    ) -> "User":
        """
        Change change user's attribute `is_author`,
        depending on `author_status: bool` parameter.
        """
        return await self.user_repo.update(
            update_dict={"is_author": author_status},
            filters={"username": user.username},
        )

    async def change_admin_status(
        self,
        user: "User",
        admin_status: bool,
    ) -> "User":
        """
        Change change user's attribute `is_admin`,
        depending on `admin_status: bool` parameter.
        """
        return await self.user_repo.update(
            update_dict={"is_admin": admin_status},
            filters={"username": user.username},
        )

    async def change_username_or_email(
        self,
        user: "User",
        user_update: UserUpdate,
    ) -> "User":
        """
        Change user's username
        if `new_username` is the same as the ole one.

        Raise `http_400_bad_request` exception if profided
        `username` already exists.
        """
        if (
            user.username == user_update.username
            or user.email == user_update.email
        ):
            return user
        try:
            return await self.user_repo.update(
                update_dict=user_update.model_dump,
                filters={"username": user.username},
            )
        except IntegrityError as error:
            orig_detail = error.__dict__["orig"]
            error_field = str(orig_detail).split("\"")[3]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with {error_field} already exists!",
            )

    async def delete_user(self, user: "User") -> None:
        """
        Delete user.
        """
        await self.user_repo.delete({"username": user.username})
