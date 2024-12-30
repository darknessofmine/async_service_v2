from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from .repositories import UserRepo
from .schemas import UserCreate
from api.auth import utils as auth_utils


if TYPE_CHECKING:
    from core.models import User


class UserService:
    def __init__(
        self,
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
    ) -> None:
        self.user_repo: UserRepo = user_repo

    async def create_superuser(self,
                               user: UserCreate) -> "User":
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
