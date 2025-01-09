from datetime import datetime

from sqlalchemy import ForeignKey, func, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IntIdPkMixin


class Comment(Base, IntIdPkMixin):
    __tablename__ = "comments"

    text: Mapped[str] = mapped_column(String(500))
    created: Mapped[datetime] = mapped_column(default=func.now())
    updated: Mapped[datetime] = mapped_column(
        onupdate=func.now(),
        nullable=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"),
    )
