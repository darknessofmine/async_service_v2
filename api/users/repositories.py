from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from api.utils.repositories import (
    CreateRepo,
    GetOneRepo,
    DeleteRepo,
    UpdateRepo,
)
from core.models import User


class UserRepo(CreateRepo[User],
               GetOneRepo[User],
               UpdateRepo[User],
               DeleteRepo[User]):
    model = User

    async def get_one_with_token(
        self,
        filters: dict[str, Any],
    ) -> User | None:
        stmt = select(self.model).options(joinedload(self.model.token))
        for key, value in filters.items():
            if hasattr(self.model, key):
                stmt = stmt.filter(getattr(self.model, key) == value)
        return await self.session.scalar(stmt)

    async def get_one_with_profile(
        self,
        filters: dict[str, Any],
    ) -> User | None:
        stmt = select(self.model).options(joinedload(self.model.profile))
        for key, value in filters.items():
            if hasattr(self.model, key):
                stmt = stmt.filter(getattr(self.model, key) == value)
        return await self.session.scalar(stmt)
