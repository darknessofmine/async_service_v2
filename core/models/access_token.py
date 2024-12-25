from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from core.settings import settings


if TYPE_CHECKING:
    from core.models import User


class AccessToken(Base):
    __tablename__ = "access_tokens"

    token: Mapped[str] = mapped_column(String(512), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    expired: Mapped[datetime] = mapped_column(
        default=func.now() + timedelta(
            days=settings.auth.jwt.refresh_token_expire_days
        ),
        index=True,
    )

    user: Mapped["User"] = relationship(back_populates="token")
