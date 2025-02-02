from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.exc import IntegrityError

from .repositories import UserRepo
from .schemas import UserCreate, UserUpdate
from api.auth import utils as auth_utils
from api.utils.schemas import PropertyFilter
from core.models import Comment, Post, SubTier, User


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
    async def get_user_by_username(
        username: Annotated[str, Path],
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
    ) -> "User":
        user = await user_repo.get_one(
            filters={"username": username},
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with such username doesn't exist.",
            )
        return user


class GetUserWithObjId:
    RELATED_MODELS_BY_OBJ_NAME = {
        "comment": User.comments,
        "post": User.posts,
        "sub_tier": User.sub_tiers,
    }

    RELATED_MODELS_ID_BY_OBJ_NAME = {
        "comment": Comment.id,
        "post": Post.id,
        "sub_tier": SubTier.id,
    }

    def __init__(self, obj_name: str) -> None:
        if obj_name not in self.RELATED_MODELS_BY_OBJ_NAME:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        self.obj_name = obj_name

    async def __call__(
        self,
        username: Annotated[str, Path],
        obj_id: Annotated[int, Path],
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
    ) -> User | None:
        user = await user_repo.get_one(
            filters={"username": username},
            property_filter=PropertyFilter(
                related_model=self.RELATED_MODELS_BY_OBJ_NAME[self.obj_name],
                model_field=self.RELATED_MODELS_ID_BY_OBJ_NAME[self.obj_name],
                field_value=obj_id,
                return_model=True,
            )
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"User '{username}' doesn't have "
                    f"{self.obj_name} with id={obj_id}."
                ),
            )
        return user
