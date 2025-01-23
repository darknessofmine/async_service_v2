from typing import Annotated

from fastapi import APIRouter, Depends, status

from .schemas import SubscriptionResponse
from .services import SubscriptionService
from api.auth.services import AuthService
from api.users.services import GetUserWithObjId
from core.models.user import User


router = APIRouter(
    tags=["subscripton"],
)


@router.post("/{username}/subscribe/{obj_id}",
             response_model=SubscriptionResponse,
             status_code=status.HTTP_200_OK)
async def subscribe(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    sub_owner: Annotated[User, Depends(GetUserWithObjId("sub_tier"))],
    sub_service: Annotated[SubscriptionService, Depends(SubscriptionService)],
) -> SubscriptionResponse:
    return await sub_service.create_update_manager(
        owner_id=sub_owner.id,
        client_id=current_user.id,
        sub_tier_id=sub_owner.sub_tiers[0].id,
    )
