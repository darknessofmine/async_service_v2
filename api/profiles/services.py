from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException, status

from . import schemas
from .repositories import ProfileRepo
from api.users.repositories import UserRepo


if TYPE_CHECKING:
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
        return await self.profile_repo.update(
            update_dict=profile_update.model_dump(),
            filters={"user_id": user.id},
        )

    async def get_user_profile_by_username(self, username: str) -> "Profile":
        """
        Get user's profile by their username.

        Raise `http_404_not_found` exception,
        if user with profile doesn't have `is_author` status.
        """
        user = await self.user_repo.get_one_with_profile(
            filters={"username": username},
        )
        if user is None or not user.is_author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=("Only verified users with `author` status "
                        "are allowed to have profile.")
            )
        return user.profile

    async def change_profile_name_on_username_change(
        self,
        user: "User",
        new_username: str,
    ) -> None:
        """
        Change user's `profile.first_name` to `user.username`

        Do nothing if current username is the same as the new_username,
        or if user already has custom profile name.
        """
        if user.profile.first_name == user.username != new_username:
            await self.profile_repo.update(
                update_dict={
                    "first_name": new_username,
                    "last_name": None,
                },
                filters={"user_id": user.id},
            )
