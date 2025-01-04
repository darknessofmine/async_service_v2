from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import joinedload, contains_eager

from api.utils.repositories import (
    CreateRepo,
    GetOneRepo,
    DeleteRepo,
    UpdateRepo,
)
from core.models import User, SubTier


class UserRepo(CreateRepo[User],
               GetOneRepo[User],
               UpdateRepo[User],
               DeleteRepo[User]):
    model = User

    async def get_one_with_token(
        self,
        filters: dict[str, Any],
    ) -> User | None:
        stmt = select(User).options(joinedload(User.token))
        for key, value in filters.items():
            if hasattr(User, key):
                stmt = stmt.filter(getattr(User, key) == value)
        return await self.session.scalar(stmt)

    async def get_one_with_profile(
        self,
        filters: dict[str, Any],
    ) -> User | None:
        stmt = select(User).options(joinedload(User.profile))
        for key, value in filters.items():
            if hasattr(User, key):
                stmt = stmt.filter(getattr(User, key) == value)
        return await self.session.scalar(stmt)

    async def get_one_with_sub_tier_id(
        self,
        filters: dict[str, Any],
        sub_tier_id: int,
    ) -> User | None:
        stmt = (
            select(User)
            .join(User.sub_tiers).options(contains_eager(User.sub_tiers))
        ).filter(SubTier.id == sub_tier_id)
        for key, value in filters.items():
            if hasattr(User, key):
                stmt = stmt.filter(getattr(User, key) == value)
        return await self.session.scalar(stmt)
