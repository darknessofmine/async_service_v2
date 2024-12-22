from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from core.models import Base


class CreateRepo:
    model: Base = None

    async def create(self, data_dict: dict, session: AsyncSession) -> Base:
        new_obj = self.model(**data_dict)
        session.add(new_obj)
        await session.commit()
        return new_obj


class DeleteRepo:
    model: Base = None

    async def delete(self, session: AsyncSession) -> None:
        await session.delete(self.model)
        await session.commit()
