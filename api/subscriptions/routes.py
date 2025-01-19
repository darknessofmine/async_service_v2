from typing import Annotated

from fastapi import APIRouter, Depends, status

from .schemas import SubscriptionResponse
from .services import SubscriptionService
from api.auth.services import AuthService
from api.sub_tiers.services import SubTierService
from api.users.services import UserService
from core.models.user import User


router = APIRouter(
    tags=["subscripton"],
)


@router.post("/{username}/subscribe/{sub_tier_id}",
             response_model=SubscriptionResponse,
             status_code=status.HTTP_200_OK)
async def subscribe(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    user_service: Annotated[UserService, Depends(UserService)],
    sub_service: Annotated[SubscriptionService, Depends(SubscriptionService)],
    sub_tier_service: Annotated[SubTierService, Depends(SubTierService)],
    username: str,
    sub_tier_id: int,
) -> SubscriptionResponse:
    owner = await user_service.get_user_by_username_with_sub_tiers(username)
    sub_tier_service.user_has_sub_tier_or_404(owner, sub_tier_id)
    return await sub_service.create_subscription(
        owner_id=owner.id,
        sub_id=current_user.id,
        sub_tier_id=sub_tier_id,
    )
