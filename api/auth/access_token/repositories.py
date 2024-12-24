from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.repositories import CreateRepo, DeleteRepo
from core.models import AccessToken


class AccessTokenRepo(CreateRepo[AccessToken],
                      DeleteRepo[AccessToken]):
    model = AccessToken

    async def get_one_with_user(
        self,
        filters: dict[str, Any],
        session: AsyncSession,
    ) -> AccessToken | None:
        stmt = select(self.model).options(joinedload(self.model.user))
        for key, value in filters.items():
            if hasattr(self.model, key):
                stmt = stmt.filter(getattr(self.model, key) == value)
        return await session.scalar(stmt)
