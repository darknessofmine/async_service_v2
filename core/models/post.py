from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin


if TYPE_CHECKING:
    from core.models import Comment, SubTier, User


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

    user: Mapped["User"] = relationship(back_populates="posts")
    sub_tier: Mapped["SubTier"] = relationship(back_populates="posts")
    comments: Mapped["Comment"] = relationship(back_populates="post")
