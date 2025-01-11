from typing import Annotated

from fastapi import Depends

from .repositories import CommentRepo
from .schemas import CommentCreate, CommentUpdate
from core.models import Comment, User


class CommentService:
    def __init__(
        self,
        comment_repo: Annotated[CommentRepo, Depends(CommentRepo)]
    ) -> None:
        self.__comment_repo = comment_repo

    async def create_comment(
        self,
        user: User,
        comment: CommentCreate,
    ) -> Comment:
        comment_create_dict = comment.model_dump()
        comment_create_dict["user_id"] = user.id
        return await self.__comment_repo.create(comment_create_dict)

    async def update_comment(
        self,
        comment_update: CommentUpdate,
        comment_id: int,
    ) -> Comment:
        return await self.__comment_repo.update(
            update_dict=comment_update.model_dump(),
            filters={"id": comment_id},
            return_result=True,
        )

    async def delete_comment(self, comment_id: int) -> None:
        await self.__comment_repo.delete(filters={"id": comment_id})
