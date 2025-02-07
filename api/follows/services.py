from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from .repositories import FollowRepo
from core.models import Follow


class FollowService:
    def __init__(
        self,
        follow_repo: Annotated[FollowRepo, Depends(FollowRepo)],
    ) -> None:
        self.follow_repo = follow_repo

    async def create_followage(self, client_id: int, owner_id: int) -> Follow:
        create_dict = {
            "owner_id": owner_id,
            "client_id": client_id,
        }
        try:
            return await self.follow_repo.create(create_dict)
        except IntegrityError as error:
            orig_detail = error.__dict__["orig"]
            error_field = str(orig_detail).split("\"")[3]
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Followage with {error_field} already exists!",
            )

    async def delete_followage(self, client_id: int, owner_id: int) -> None:
        delete_dict = {
            "owner_id": owner_id,
            "client_id": client_id,
        }
        await self.follow_repo.delete(delete_dict)
