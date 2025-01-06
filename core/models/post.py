from datetime import datetime

from sqlalchemy import ForeignKey, func, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IntIdPkMixin


class Post(Base, IntIdPkMixin):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(String(128))
    text: Mapped[str] = mapped_column(Text, nullable=True)
    file_url: Mapped[str] = mapped_column(String, nullable=True)
    created: Mapped[datetime] = mapped_column(default=func.now())
    updated: Mapped[datetime] = mapped_column(
        onupdate=func.now(),
        nullable=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    sub_tier_id: Mapped[int] = mapped_column(
        ForeignKey("sub_tiers.id", ondelete="SET NULL"),
        nullable=True,
    )
