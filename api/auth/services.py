from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .access_token import utils as token_utils
from .access_token.repositories import AccessTokenRepo
from api.users import schemas as user_schemas
from api.users.repositories import UserRepo
from core.database import db
from core.settings import settings


if TYPE_CHECKING:
    from core.models import AccessToken, User


class AuthService:
    def __init__(
        self,
        token_repo: Annotated[AccessTokenRepo, Depends(AccessTokenRepo)],
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
        session: Annotated[AsyncSession, Depends(db.get_async_session)],
    ) -> None:
        self.token_repo: AccessTokenRepo = token_repo
        self.user_repo: UserRepo = user_repo
        self.session: AsyncSession = session

    # Crete new user
    async def create_user(self,
                          user_create: user_schemas.UserCreate) -> "User":
        user_dict = user_create.model_dump()
        return await self.user_repo.create(user_dict, self.session)

    # Get user by username and password (with token),
    # raise exception if user does't exist.
    async def validate_auth_user(self,
                                 user: user_schemas.UserLogin) -> "User":
        validated_user = await self.user_repo.get_one_with_token(
            filters=user.model_dump(),
            session=self.session,
        )
        if validated_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password!",
            )
        return validated_user

    # Create and return new token for validated user if it doesn't exist yet,
    # otherwise get and return current token.
    async def get_access_token_for_user(
        self,
        user: user_schemas.UserLogin
    ) -> "AccessToken":
        validated_user = await self.validate_auth_user(user)
        if validated_user.token is not None:
            return validated_user.token
        token_dict = {
            "token": str(token_utils.generate_uuid_access_token()),
            "user_id": validated_user.id,
        }
        return await self.token_repo.create(token_dict, self.session)


class UserValidationService:
    def __init__(
        self,
        token: Annotated[str, Depends(settings.auth.oauth2_scheme)],
        token_repo: Annotated[AccessTokenRepo, Depends(AccessTokenRepo)],
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
        session: Annotated[AsyncSession, Depends(db.get_async_session)],
    ) -> None:
        self.token = token
        self.token_repo: AccessTokenRepo = token_repo
        self.user_repo: UserRepo = user_repo
        self.session: AsyncSession = session

    async def get_token_payload(self):
        ...
