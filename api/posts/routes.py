from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Path, UploadFile, status

from .schemas import PostCreate, PostResponse, PostUpdate, PostUpdateResponse
from .services import PostService
from api.auth.permissions import IsOwner, Permissions
from api.users.services import GetUserWithObjId
from background_tasks.files.file_service import file_service
from core.models.user import User

router = APIRouter(
    tags=["posts"],
)


@router.post("/posts/",
             response_model=PostResponse,
             status_code=status.HTTP_201_CREATED)
async def create_post(
    user: Annotated[User, Depends(Permissions("is_author"))],
    post_service: Annotated[PostService, Depends(PostService)],
    title: str = Form(...),
    text: str | None = Form(None),
    sub_tier_id: int | None = Form(None),
    file: Annotated[UploadFile | str | None, File()] = None,
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


@router.get("/{username}/posts/{obj_id}",
            response_model=PostResponse,
            status_code=status.HTTP_200_OK)
async def get_one_post(
    post_service: Annotated[PostService, Depends(PostService)],
    post_owner: Annotated[User, Depends(GetUserWithObjId("post"))],
) -> PostResponse:
    return await post_service.get_post(post_id=post_owner.posts[0].id)


@router.get("/{username}/posts",
            response_model=list[PostResponse],
            status_code=status.HTTP_200_OK)
async def get_all_user_posts(
    post_service: Annotated[PostService, Depends(PostService)],
    username: Annotated[str, Path],
) -> list[PostResponse]:
    return await post_service.get_user_posts_by_username(username)


@router.patch("/posts/{obj_id}",
              response_model=PostUpdateResponse,
              status_code=status.HTTP_200_OK)
async def update_post(
    user: Annotated[User, Depends(IsOwner("post"))],
    post_service: Annotated[PostService, Depends(PostService)],
    title: str = Form(None),
    text: str = Form(None),
    sub_tier_id: int | None = Form(None),
    file: Annotated[UploadFile | str | None, File()] = None,
) -> PostUpdateResponse:
    file_url = file_service.get_post_file_url(file)
    # TODO: Finish backgruond file save.
    file_service.save_file(file, file_url)
    post_update = PostUpdate(
        title=title,
        text=text,
        file_url=file_url,
        sub_tier_id=sub_tier_id,
    )
    return await post_service.update_post(
        post_update=post_update,
        post_id=user.posts[0].id,
    )


@router.delete("/posts/{obj_id}")
async def delete_post(
    user: Annotated[User, Depends(IsOwner("post"))],
    post_service: Annotated[PostService, Depends(PostService)],
) -> None:
    await post_service.delete_post(post_id=user.posts[0].id)
