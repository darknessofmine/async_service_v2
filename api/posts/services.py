from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import Sequence

from .repositories import PostRepo
from .schemas import PostCreate, PostUpdate
from api.utils.schemas import PropertyFilter
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
        post = await self.post_repo.get_one(
            filters={"id": post_id},
            related_o2m_models=[Post.comments],
        )
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(f"Post with id={post_id} not found."),
            )
        return post

    async def get_user_posts_by_username(
        self,
        username: str,
    ) -> Sequence[Post]:
        posts = await self.post_repo.get_many(
            property_filter=PropertyFilter(
                related_model=Post.user,
                model_field=User.username,
                field_value=username,
            ),
            related_o2m_models=[Post.comments],
            order_by="created",
        )
        if posts is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User `{username}` not found.",
            )
        return posts.all()

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
