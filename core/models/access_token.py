from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[int]):
    __tablename__ = "access_tokens"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    @classmethod
    async def get_db(cls,
                     session: AsyncSession) -> SQLAlchemyAccessTokenDatabase:
        return SQLAlchemyAccessTokenDatabase(session, cls)
