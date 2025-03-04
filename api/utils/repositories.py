from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import delete, select, Sequence, text, update
from sqlalchemy.orm import (
    contains_eager,
    joinedload,
    Relationship,
    selectinload,
)
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import PropertyFilter
from core.database import db
from core.models import Base


class BaseRepo:
    model: Base = None

    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(db.get_async_session)],
    ) -> None:
        self.session = session

    def _apply_filters(
        self,
        stmt: Any,
        filters: dict[str, Any],
    ) -> Any:
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    stmt = stmt.filter(getattr(self.model, key) == value)
        return stmt

    @staticmethod
    def _apply_property_filter(
        stmt: Any,
        prop_filter: PropertyFilter,
    ) -> Any:
        if prop_filter:
            stmt = stmt.join(prop_filter.related_model)
            if prop_filter.return_model:
                stmt = stmt.options(contains_eager(prop_filter.related_model))
            stmt = stmt.filter(
                prop_filter.model_field == prop_filter.field_value
            )
        return stmt

    @staticmethod
    def _add_related_o2o_models(
        stmt: Any,
        related_o2o_models: list[Relationship] | None,
    ) -> Any:
        if related_o2o_models:
            for related_model in related_o2o_models:
                stmt = stmt.options(joinedload(related_model))
        return stmt

    @staticmethod
    def _add_related_o2m_models(
        stmt: Any,
        related_o2m_models: list[Relationship] | None,
    ) -> Any:
        if related_o2m_models:
            for related_model in related_o2m_models:
                stmt = stmt.options(selectinload(related_model))
        return stmt


class CreateRepo[T](BaseRepo):
    async def create(
        self,
        data_dict: dict[str, Any],
    ) -> T:
        new_obj = self.model(**data_dict)
        self.session.add(new_obj)
        await self.session.commit()
        return new_obj


class GetOneRepo[T](BaseRepo):
    async def get_one(
        self,
        filters: dict[str, Any],
        property_filter: PropertyFilter | None = None,
        related_o2o_models: list[Relationship] | None = None,
        related_o2m_models: list[Relationship] | None = None,
    ) -> T | None:
        stmt = select(self.model)
        stmt = self._add_related_o2o_models(stmt, related_o2o_models)
        stmt = self._add_related_o2m_models(stmt, related_o2m_models)
        stmt = self._apply_property_filter(stmt, property_filter)
        stmt = self._apply_filters(stmt, filters)
        return await self.session.scalar(stmt)


class GetManyRepo[T](BaseRepo):
    @staticmethod
    def _add_limit(stmt: Any, limit: int | None) -> Any:
        if limit is not None:
            stmt = stmt.limit(limit)
        return stmt

    @staticmethod
    def _add_offset(stmt: Any, offset: int | None) -> Any:
        if offset is not None:
            stmt = stmt.offset(offset)
        return stmt

    @staticmethod
    def _apply_order(stmt: Any, order_by_field: str | None) -> Any:
        if order_by_field:
            if order_by_field[0] == "-":
                stmt = stmt.order_by(
                    text(f"{order_by_field.replace("-", "")} desc"),
                )
            else:
                stmt = stmt.order_by(text(order_by_field))
        return stmt

    async def get_many(
        self,
        filters: dict[str, Any] | None = None,
        property_filter: PropertyFilter | None = None,
        related_o2o_models: list[Relationship] | None = None,
        related_o2m_models: list[Relationship] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        order_by: str | None = None,
    ) -> Sequence[T] | None:
        stmt = select(self.model)
        stmt = self._add_related_o2o_models(stmt, related_o2o_models)
        stmt = self._add_related_o2m_models(stmt, related_o2m_models)
        stmt = self._apply_property_filter(stmt, property_filter)
        stmt = self._apply_filters(stmt, filters)
        stmt = self._add_limit(stmt, limit)
        stmt = self._add_offset(stmt, offset)
        stmt = self._apply_order(stmt, order_by)
        return await self.session.scalars(stmt)


class UpdateRepo[T](BaseRepo):
    async def update(
        self,
        update_dict: dict[str, Any],
        filters: dict[str, Any],
        return_result: bool = False,
    ) -> T | None:
        stmt = update(self.model).values(update_dict)
        stmt = self._apply_filters(stmt, filters)
        if return_result:
            updated = await self.session.scalar(stmt.returning(self.model))
            await self.session.commit()
            return updated
        else:
            await self.session.execute(stmt)
            await self.session.commit()


class DeleteRepo[T](BaseRepo):
    async def delete(
        self,
        filters: dict[str, Any],
        return_result: bool = False,
    ) -> T | None:
        stmt = delete(self.model)
        stmt = self._apply_filters(stmt, filters)
        if return_result:
            deleted = await self.session.scalar(stmt.returning(self.model))
            await self.session.commit()
            return deleted
        else:
            await self.session.execute(stmt)
            await self.session.commit()
