from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.exc import IntegrityError

from .repositories import UserRepo
from .schemas import UserCreate, UserUpdate
from api.auth import utils as auth_utils
from core.models import User


class UserService:
    def __init__(
        self,
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
    ) -> None:
        self.user_repo: UserRepo = user_repo

    async def create_superuser(self, user: UserCreate) -> User:
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
        user: User,
        author_status: bool,
    ) -> User:
        """
        Change change user's attribute `is_author`,
        depending on `author_status: bool` parameter.
        """
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has to be verified."
            )
        return await self.user_repo.update(
            update_dict={"is_author": author_status},
            filters={"username": user.username},
            return_result=True,
        )

    async def get_user_by_username_with_sub_tiers(
        self,
        username: str,
    ) -> User | None:
        user = await self.user_repo.get_one(
            filters={"username": username},
            related_o2m_models=[User.sub_tiers],
        )
        if user is not None and user.is_author:
            return user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(f"User `{username}` doesn't exist "
                    "or doesn't have author status"),
        )

    async def change_admin_status(
        self,
        user: User,
        admin_status: bool,
    ) -> User:
        """
        Change change user's attribute `is_admin`,
        depending on `admin_status: bool` parameter.
        """
        return await self.user_repo.update(
            update_dict={"is_admin": admin_status},
            filters={"username": user.username},
            return_result=True,
        )

    async def change_user_email(
        self,
        user: User,
        user_update: UserUpdate,
    ) -> User:
        """
        Change user's email.

        Raise `http_400_bad_request` exception if provided
        `email` already exists or is the same as the old one.
        """
        if user.email == user_update.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have this email.",
            )
        try:
            return await self.user_repo.update(
                update_dict=user_update.model_dump(exclude_unset=True),
                filters={"username": user.username},
                return_result=True,
            )
        except IntegrityError as error:
            orig_detail = error.__dict__["orig"]
            error_field = str(orig_detail).split("\"")[3]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with {error_field} already exists!",
            )

    async def delete_user(self, user: User) -> None:
        """
        Delete user.
        """
        await self.user_repo.delete(filters={"username": user.username})

    @staticmethod
    async def check_user_owns_post(
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
        username: Annotated[str, Path],
        post_id: Annotated[int, Path],
    ) -> User | None:
        user = await user_repo.get_one_with_related_obj_id(
            filters={"username": username},
            related_model=User.posts,
            related_model_id=post_id,
        )
        if user is not None:
            return user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User ({username}) doesn't have post with id={post_id}.",
        )
