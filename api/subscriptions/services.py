from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from .repositories import SubsciptionRepo
from core.models import Subscription


class SubscriptionService:
    def __init__(
        self,
        sub_repo: Annotated[SubsciptionRepo, Depends(SubsciptionRepo)],
    ) -> None:
        self.sub_repo = sub_repo

    async def create_update_manager(
        self,
        owner_id: int,
        client_id: int,
        sub_tier_id: int | None = None,
    ) -> Subscription:
        if owner_id == client_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can't subscribe yourself.",
            )
        subscription = await self.get_one_or_none_by_client_owner_id(
            owner_id=owner_id,
            client_id=client_id,
        )
        if subscription is not None:
            if subscription.sub_tier_id != sub_tier_id:
                return await self.change_subscription_tier(
                    subscrption_id=subscription.id,
                    sub_tier_id=sub_tier_id,
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have chosen subscription tier.",
            )
        else:
            return await self.create_subscription(
                owner_id=owner_id,
                client_id=client_id,
                sub_tier_id=sub_tier_id,
            )

    async def create_subscription(
        self,
        owner_id: int,
        client_id: int,
        sub_tier_id: int | None = None,
    ) -> Subscription:
        create_dict = {
            "owner_id": owner_id,
            "sub_id": client_id,
            "sub_tier_id": sub_tier_id,
        }
        try:
            return await self.sub_repo.create(create_dict)
        except IntegrityError as error:
            orig_detail = error.__dict__["orig"]
            error_field = str(orig_detail).split("\"")[3]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Subscription with {error_field} already exists!",
            )

    async def get_one_or_none_by_client_owner_id(
        self,
        owner_id: int,
        client_id: int,
    ) -> Subscription | None:
        return await self.sub_repo.get_one(
            filters={
                "owner_id": owner_id,
                "sub_id": client_id,
            }
        )

    async def change_subscription_tier(
        self,
        subscrption_id: int,
        sub_tier_id: int,
    ) -> Subscription:
        return await self.sub_repo.update(
            update_dict={"sub_tier_id": sub_tier_id},
            filters={"id": subscrption_id},
            return_result=True,
        )

    async def delete_subsciption(self, subscrption_id: int) -> None:
        await self.sub_repo.delete(filters={"id": subscrption_id})
