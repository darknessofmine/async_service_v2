from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from .repositories import SubTierRepo
from .schemas import SubTierCreate


if TYPE_CHECKING:
    from core.models import SubTier, User


class SubTierService:
    def __init__(
        self,
        sub_tier_repo: Annotated[SubTierRepo, Depends(SubTierRepo)],
    ) -> None:
        self.sub_tier_repo = sub_tier_repo

    async def create_sub_tier(
        self,
        user: "User",
        sub_tier: SubTierCreate,
    ) -> "SubTier":
        sub_tier_dict = sub_tier.model_dump()
        if not sub_tier_dict["image_url"]:
            sub_tier_dict.pop("image_url")
        sub_tier_dict["user_id"] = user.id
        try:
            return await self.sub_tier_repo.create(sub_tier_dict)
        except IntegrityError as error:
            orig_detail = error.__dict__["orig"]
            error_field = str(orig_detail).split("\"")[3]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Subscription with {error_field} already exists!",
            )
