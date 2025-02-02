from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from . import utils
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
        utils.client_is_not_sub_owner_or_403(client_id, owner_id)
        subscription = await self.sub_repo.get_one(
            filters={
                "owner_id": owner_id,
                "sub_id": client_id,
            },
        )
        if subscription is not None:
            if subscription.sub_tier_id != sub_tier_id:
                return await self.change_subscription_tier(
                    subscrption_id=subscription.id,
                    sub_tier_id=sub_tier_id,
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already subscribed to chosen tier.",
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

    async def change_subscription_tier(
        self,
        subscrption_id: int,
        sub_tier_id: int,
    ) -> Subscription | None:
        return await self.sub_repo.update(
            update_dict={"sub_tier_id": sub_tier_id},
            filters={"id": subscrption_id},
            return_result=True,
        )

    async def unsubscribe_from_current_tier(
        self,
        owner_id: int,
        client_id: int,
        sub_tier_id: int,
    ) -> None:
        utils.client_is_not_sub_owner_or_403(client_id, owner_id)
        subscription = await self.sub_repo.get_one(
            filters={
                "owner_id": owner_id,
                "sub_id": client_id,
            },
        )
        if subscription:
            if subscription.sub_tier_id == sub_tier_id:
                return await self.change_subscription_tier(
                    subscrption_id=subscription.id,
                    sub_tier_id=None,
                )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You are not subscribed to chosen tier."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not subscribed to any tier.",
        )

    async def follow(self, owner_id: int, client_id: int) -> Subscription:
        utils.client_is_not_sub_owner_or_403(client_id, owner_id)
        data_dict = {
            "owner_id": owner_id,
            "sub_id": client_id,
        }
        subscription = await self.sub_repo.get_one(filters=data_dict)
        if subscription:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already subscribed.",
            )
        return await self.sub_repo.create(data_dict)

    async def delete_subsciption(self, subscrption_id: int) -> None:
        await self.sub_repo.delete(filters={"id": subscrption_id})
