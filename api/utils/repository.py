from typing import Any, TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from core.models import Base


class CreateRepo:
    model: "Base" = None

    async def create(self, data_dict: dict, session: AsyncSession) -> "Base":
        new_obj = self.model(**data_dict)
        session.add(new_obj)
        await session.commit()
        return new_obj


class GetOneRepo:
    model: "Base" = None

    async def get_one(
        self,
        filters: dict[str, Any],
        session: AsyncSession,
    ) -> "Base":
        stmt = select(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                stmt = stmt.filter(getattr(self.model, key) == value)
        return await session.scalar(stmt)


class DeleteRepo:
    model: "Base" = None

    async def delete(self, session: AsyncSession) -> None:
        await session.delete(self.model)
        await session.commit()
