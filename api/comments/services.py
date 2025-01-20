from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from .repositories import CommentRepo
from .schemas import CommentCreate, CommentUpdate
from core.models import Comment, User


class CommentService:
    def __init__(
        self,
        comment_repo: Annotated[CommentRepo, Depends(CommentRepo)]
    ) -> None:
        self.comment_repo = comment_repo

    async def create_comment(
        self,
        user: User,
        comment: CommentCreate,
        post_id: int,
    ) -> Comment:
        comment_create_dict = comment.model_dump()
        comment_create_dict["user_id"] = user.id
        comment_create_dict["post_id"] = post_id
        try:
            return await self.comment_repo.create(comment_create_dict)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id={post_id} doesn't exist.",
            )

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
