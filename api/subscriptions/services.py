from typing import Annotated

from fastapi import Depends

from .repositories import SubsciptionRepo
from core.models import Subscription


class SubscriptionService:
    def __init__(
        self,
        sub_repo: Annotated[SubsciptionRepo, Depends(SubsciptionRepo)],
    ) -> None:
        self.sub_repo = sub_repo

    async def create_subscription(
        self,
        owner_id: int,
        sub_id: int,
        sub_tier_id: int | None = None,
    ) -> Subscription:
        create_sub_dict = {
            "owner_id": owner_id,
            "sub_id": sub_id,
        }
        if sub_tier_id:
            create_sub_dict["sub_tier_id"] = sub_tier_id
        return await self.sub_repo.create(create_sub_dict)

    async def change_subscription_tier(
        self,
        sub_id: int,
        sub_tier_id: int,
    ) -> Subscription:
        return await self.sub_repo.update(
            update_dict={"sub_tier_id": sub_tier_id},
            filters={"id": sub_id},
            return_result=True,
        )

    async def delete_subsciption(self, sub_id: int) -> None:
        await self.sub_repo.delete(filters={"id": sub_id})
