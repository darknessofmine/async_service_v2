from api.auth.access_token.repositories import AccessTokenRepo
from api.users.repositories import UserRepo

from api.users.schemas import UserCreate


class AuthService:
    def __init__(
        self,
        token_repo: AccessTokenRepo,
        user_repo: UserRepo,
    ):
        self.token_repo: AccessTokenRepo = token_repo
        self.user_repo: UserRepo = user_repo

    async def user_create(
        self,
        user_create: UserCreate,
    ):
        ...
