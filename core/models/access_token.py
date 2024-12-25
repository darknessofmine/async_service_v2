from datetime import datetime, timedelta

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from core.settings import settings


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
