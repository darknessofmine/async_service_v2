from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from .repositories import SubTierRepo
from .schemas import SubTierCreate, SubTierUpdate
from api.users.repositories import UserRepo
from core.models import SubTier, User


class SubTierService:
    def __init__(
        self,
        sub_tier_repo: Annotated[SubTierRepo, Depends(SubTierRepo)],
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
    ) -> None:
        self.sub_tier_repo = sub_tier_repo
        self.user_repo = user_repo

    async def create_sub_tier(
        self,
        user: "User",
        sub_tier: SubTierCreate,
    ) -> "SubTier":
        sub_tier_dict = sub_tier.model_dump()
        sub_tier_dict["user_id"] = user.id
        if not sub_tier_dict["image_url"]:
            sub_tier_dict.pop("image_url")
        try:
            return await self.sub_tier_repo.create(sub_tier_dict)
        except IntegrityError as error:
            orig_detail = error.__dict__["orig"]
            error_field = str(orig_detail).split("\"")[3]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Subscription with {error_field} already exists!",
            )

    async def get_sub_tier_list_by_username(
        self,
        username: str,
    ) -> list["SubTier"]:
        user = await self.user_repo.get_one(
            filters={"username": username},
            related_o2m_models=[User.sub_tiers],
        )
        if user.is_author:
            return user.sub_tiers
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested user is not an author."
        )

    async def update_sub_tier(
        self,
        sub_tier_update: SubTierUpdate,
        sub_tier_id: int,
    ) -> "SubTier":
        update_dict = dict()
        for key, value in sub_tier_update.model_dump().items():
            if sub_tier_update.model_dump()[key]:
                update_dict[key] = value
        return await self.sub_tier_repo.update(
            update_dict=update_dict,
            filters={"id": sub_tier_id},
            return_result=True,
        )

    async def delete_sub_tier(self, sub_tier_id: int) -> None:
        await self.sub_tier_repo.delete(filters={"id": sub_tier_id})
