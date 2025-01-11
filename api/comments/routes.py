from typing import Annotated

from fastapi import APIRouter, Depends, status

from .schemas import CommentCreate, CommentResponse, CommentUpdate
from .services import CommentService
from api.auth.permissions import IsOwner, Permissions
from core.models import User


router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)


@router.post("/",
             response_model=CommentResponse,
             status_code=status.HTTP_201_CREATED)
async def create_comment(
    user: Annotated[User, Depends(Permissions(["is_verified"]))],
    comment_service: Annotated[CommentService, Depends(CommentService)],
    comment: CommentCreate,
) -> CommentResponse:
    return await comment_service.create_comment(user, comment)


@router.patch("/{comment_id}",
              response_model=CommentResponse,
              status_code=status.HTTP_200_OK)
async def update_comment(
    user: Annotated[User, Depends(IsOwner("comment"))],
    comment_service: Annotated[CommentService, Depends(CommentService)],
    comment_update: CommentUpdate,
) -> CommentResponse:
    return await comment_service.update_comment(
        comment_update=comment_update,
        comment_id=user.comments[0].id,
    )


@router.delete("/{comment_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    user: Annotated[User, Depends(IsOwner("comment"))],
    comment_service: Annotated[CommentService, Depends(CommentService)],
) -> None:
    await comment_service.delete_comment(comment_id=user.comments[0].id)
