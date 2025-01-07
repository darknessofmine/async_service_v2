from typing import Annotated

from fastapi import Depends

from .repositories import PostRepo
from .schemas import PostCreate, PostUpdate
from core.models import User, Post


class PostService:
    def __init__(
        self,
        post_repo: Annotated[PostRepo, Depends(PostRepo)],
    ) -> None:
        self.post_repo = post_repo

    async def create_post(self, user: User, post: PostCreate) -> Post:
        create_dict = dict()
        for key, value in post.model_dump().items():
            if post.model_dump()[key]:
                create_dict[key] = value
        create_dict["user_id"] = user.id
        return await self.post_repo.create(create_dict)

    async def get_post(self, post_id: int) -> Post:
        return await self.post_repo.get_one(filters={"id": post_id})

    async def update_post(self, post_update: PostUpdate, post_id: int) -> Post:
        update_dict = dict()
        for key, value in post_update.model_dump().items():
            if post_update.model_dump()[key]:
                update_dict[key] = value
        return await self.post_repo.update(
            update_dict=update_dict,
            filters={"id": post_id},
            return_result=True,
        )

    async def delete_post(self, post_id: int) -> None:
        await self.post_repo.delete(filters={"id": post_id})
