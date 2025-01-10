from typing import Annotated

from fastapi import Depends

from .repositories import CommentRepo
from .schemas import CommentCreate, CommentUpdate
from core.models import Comment


class CommentService:
    def __init__(
        self,
        comment_repo: Annotated[CommentRepo, Depends(CommentRepo)]
    ) -> None:
        self.comment_repo = comment_repo

    async def craete_comment(self, comment_create: CommentCreate) -> Comment:
        return await self.comment_repo.create(**comment_create.model_dump())

    async def update_comment(
        self,
        comment_update: CommentUpdate,
        comment_id: int,
    ) -> Comment:
        return await self.comment_repo.update(
            update_dict=comment_update.model_dump(),
            filters={"id": comment_id},
            return_result=True,
        )

    async def delete_comment(self, comment_id: int) -> None:
        await self.comment_repo.delete(filters={"id": comment_id})
