from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from .schemas import PostCreate, PostResponse
from .services import PostService
from api.auth.permissions import IsOwner, Permissions
from background_tasks.files.file_service import file_service
from core.models.user import User

router = APIRouter(
    prefix="posts",
    tags=["posts"],
)


@router.post("/",
             response_model=PostResponse,
             status_code=status.HTTP_201_CREATED)
async def create_post(
    user: Annotated[User, Depends(Permissions(["is_author"]))],
    post_service: Annotated[PostService, Depends(PostService)],
    title: str = Form(...),
    text: str | None = Form(None),
    file: Annotated[UploadFile | str | None, File()] = None,
    sub_tier_id: int | None = None,
) -> PostResponse:
    file_url = file_service.get_post_file_url(file)
    # TODO: Finish backgruond file save.
    file_service.save_file(file, file_url)
    post_create = PostCreate(
        title=title,
        text=text,
        file_url=file_url,
        sub_tier_id=sub_tier_id,
    )
    return await post_service.create_post(user, post_create)


@router.delete("/{post_id}")
async def delete_post(
    user: Annotated[User, Depends(IsOwner("post"))],
    post_service: Annotated[PostService, Depends(PostService)],
) -> None:
    await post_service.delete_post(post_id=user.posts[0].id)