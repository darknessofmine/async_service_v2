from typing import Any

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class CreateRepo[T]:
    model: T = None

    async def create(self,
                     data_dict: dict[str, Any],
                     session: AsyncSession) -> T:
        new_obj = self.model(**data_dict)
        session.add(new_obj)
        await session.commit()
        return new_obj


class GetOneRepo[T]:
    model: T = None

    async def get_one(self,
                      filters: dict[str, Any],
                      session: AsyncSession) -> T | None:
        stmt = select(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                stmt = stmt.filter(getattr(self.model, key) == value)
        return await session.scalar(stmt)


class DeleteRepo[T]:
    model: T = None

    async def delete(self,
                     filters: dict[str, Any],
                     session: AsyncSession) -> None:
        stmt = delete(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                stmt = stmt.filter(getattr(self.model, key) == value)
        await session.execute(stmt)
        await session.commit()
