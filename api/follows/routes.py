from typing import Annotated

from fastapi import APIRouter, Depends, status

from .schemas import FollowResponse
from .services import FollowService
from api.auth.services import AuthService
from api.users.services import UserService
from core.models import User


router = APIRouter(
    tags=["follow"],
)


@router.post("/{username}/follow",
             response_model=FollowResponse,
             status_code=status.HTTP_200_OK)
async def follow(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    follow_owner: Annotated[User, Depends(UserService.get_user_by_username)],
    follow_service: Annotated[FollowService, Depends(FollowService)],
) -> FollowResponse:
    return await follow_service.create_followage(
        client_id=current_user.id,
        owner_id=follow_owner.id,
    )


@router.post("/{username}/unfollow",
             response_model=None,
             status_code=status.HTTP_200_OK)
async def unfollow(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    follow_owner: Annotated[User, Depends(UserService.get_user_by_username)],
    follow_service: Annotated[FollowService, Depends(FollowService)],
) -> None:
    return await follow_service.delete_followage(
        client_id=current_user.id,
        owner_id=follow_owner.id,
    )
