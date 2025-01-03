from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import delete, select, Sequence, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db


class BaseRepo:
    model = None

    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(db.get_async_session)],
    ) -> None:
        self.session = session


class CreateRepo[T](BaseRepo):
    async def create(self,
                     data_dict: dict[str, Any]) -> T:
        new_obj = self.model(**data_dict)
        self.session.add(new_obj)
        await self.session.commit()
        return new_obj


class GetOneRepo[T](BaseRepo):
    async def get_one(self,
                      filters: dict[str, Any]) -> T | None:
        stmt = select(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                stmt = stmt.filter(getattr(self.model, key) == value)
        return await self.session.scalar(stmt)


class GetManyRepo[T](BaseRepo):
    async def get_many(self,
                       filters: dict[str, Any] | None = None,
                       limit: int | None = None,
                       offset: int | None = None) -> Sequence[T] | None:
        stmt = select(self.model)
        if filters is not None:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    stmt = stmt.filter(getattr(self.model, key) == value)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        return await self.session.scalars(stmt)


class UpdateRepo[T](BaseRepo):
    async def update(self,
                     update_dict: dict[str, Any],
                     filters: dict[str, Any],
                     return_result: bool = False) -> T | None:
        stmt = update(self.model).values(update_dict)
        for key, value in filters.items():
            if hasattr(self.model, key):
                stmt = stmt.filter(getattr(self.model, key) == value)
        if return_result:
            stmt = stmt.returning(self.model)
            updated = await self.session.scalar(stmt)
            await self.session.commit()
            return updated
        else:
            await self.session.execute(stmt)
            await self.session.commit()


class DeleteRepo[T](BaseRepo):
    async def delete(self,
                     filters: dict[str, Any]) -> None:
        stmt = delete(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                stmt = stmt.filter(getattr(self.model, key) == value)
        await self.session.execute(stmt)
        await self.session.commit()
