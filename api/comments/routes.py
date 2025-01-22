from typing import Annotated

from fastapi import APIRouter, Depends, Form, status

from .schemas import CommentCreate, CommentResponse, CommentUpdate
from .services import CommentService
from api.auth.permissions import IsOwner, Permissions
from api.users.services import GetUserWithObjId
from core.models import User


router = APIRouter(
    tags=["comments"],
)


@router.post("/{username}/posts/{obj_id}/comments",
             response_model=CommentResponse,
             status_code=status.HTTP_201_CREATED)
async def create_comment(
    user: Annotated[User, Depends(Permissions("is_verified"))],
    post_owner: Annotated[User, Depends(GetUserWithObjId("post"))],
    comment_service: Annotated[CommentService, Depends(CommentService)],
    comment: CommentCreate = Form(...),
) -> CommentResponse:
    return await comment_service.create_comment(
        user=user,
        comment=comment,
        post_id=post_owner.posts[0].id,
    )


@router.patch("/comments/{obj_id}",
              response_model=CommentResponse,
              status_code=status.HTTP_200_OK)
async def update_comment(
    user: Annotated[User, Depends(IsOwner("comment"))],
    comment_service: Annotated[CommentService, Depends(CommentService)],
    comment_update: CommentUpdate = Form(...),
) -> CommentResponse:
    return await comment_service.update_comment(
        comment_update=comment_update,
        comment_id=user.comments[0].id,
    )


@router.delete("/comments/{obj_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    user: Annotated[User, Depends(IsOwner("comment"))],
    comment_service: Annotated[CommentService, Depends(CommentService)],
) -> None:
    await comment_service.delete_comment(comment_id=user.comments[0].id)
