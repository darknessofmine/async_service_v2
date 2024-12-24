from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


if TYPE_CHECKING:
    from core.models import User


class AccessToken(Base):
    __tablename__ = "access_tokens"

    token: Mapped[str] = mapped_column(String(128), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    created: Mapped[datetime] = mapped_column(
        default=func.now(),
        index=True,
    )

    user: Mapped["User"] = relationship(back_populates="token")
