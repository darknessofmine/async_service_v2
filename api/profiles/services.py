from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from . import schemas
from .repositories import ProfileRepo


if TYPE_CHECKING:
    from core.models import Profile, User


class ProfileService:
    def __init__(
        self,
        profile_repo: Annotated[ProfileRepo, Depends(ProfileRepo)],
    ) -> None:
        self.profile_repo = profile_repo

    async def create_user_profile(self, user: "User") -> None:
        profile_dict = {
            "first_name": user.username,
            "user_id": user.id,
        }
        await self.profile_repo.create(profile_dict)

    async def update_user_profile(
        self,
        user: "User",
        profile_update: schemas.ProfileUpdate,
    ) -> "Profile":
        return await self.profile_repo.update(
            update_dict=profile_update.model_dump(),
            filters={"user_id": user.id},
        )
