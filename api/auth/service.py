from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.access_token.repositories import AccessTokenRepo
from api.users.repositories import UserRepo

from api.users import schemas as user_schemas


if TYPE_CHECKING:
    from core.models import User


class AuthService:

    def __init__(
        self,
        token_repo: AccessTokenRepo,
        user_repo: UserRepo,
        session: AsyncSession,
    ) -> None:
        self.token_repo: AccessTokenRepo = token_repo()
        self.user_repo: UserRepo = user_repo()
        self.session: AsyncSession = session

    async def create_user(
        self,
        user_create: user_schemas.UserCreate,
    ) -> "User":
        user_dict = user_create.model_dump()
        return await self.user_repo.create(user_dict, self.session)
