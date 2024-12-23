from typing import Annotated

from fastapi import APIRouter, Depends, status

# from .dependencies import get_auth_service
from .service import AuthService
from api.users.schemas import UserCreate, UserResponse


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("signup",
             response_model=UserResponse,
             status_code=status.HTTP_200_OK)
async def signup(
    user_create: UserCreate,
    auth_service: Annotated[AuthService, Depends(AuthService)],
) -> UserResponse:
    return await auth_service.create_user(user_create)
