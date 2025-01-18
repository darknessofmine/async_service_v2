from typing import Annotated

from fastapi import Depends, HTTPException, status

from . import schemas
from .repositories import ProfileRepo
from api.users.repositories import UserRepo
from core.models import Profile, User


class ProfileService:
    def __init__(
        self,
        profile_repo: Annotated[ProfileRepo, Depends(ProfileRepo)],
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
    ) -> None:
        self.profile_repo: ProfileRepo = profile_repo
        self.user_repo: UserRepo = user_repo

    async def create_user_profile(self, user: "User") -> None:
        """
        Create profile for a user.
        """
        await self.profile_repo.create(
            data_dict={
                "first_name": user.username,
                "user_id": user.id,
            }
        )

    async def update_user_profile(
        self,
        user: "User",
        profile_update: schemas.ProfileUpdate,
    ) -> "Profile":
        """
        Update user profile.

        Raise `http_404_not_found` exception,
        if user with profile doesn't have `is_author` status.
        """
        if not user.is_author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Only authors are allowed to have profile."
            )
        update_dict = dict()
        for key, value in profile_update.model_dump().items():
            if profile_update.model_dump()[key] is not None:
                update_dict[key] = value
        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty values. Nothing has changed."
            )
        return await self.profile_repo.update(
            update_dict=update_dict,
            filters={"user_id": user.id},
            return_result=True,
        )

    async def get_user_profile_by_username(self, username: str) -> "Profile":
        """
        Get user's profile by their username.

        Raise `http_404_not_found` exception,
        if user doesn't exist or doesn't have `is_author` status.
        """
        user = await self.user_repo.get_one(
            filters={"username": username},
            related_o2o_models=[User.profile],
        )
        if user is None or not user.is_author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=("Only verified users with `author` status "
                        "are allowed to have profile.")
            )
        return user.profile
