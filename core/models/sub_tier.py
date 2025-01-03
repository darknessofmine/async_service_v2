from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IntIdPkMixin


class SubTier(Base, IntIdPkMixin):
    __tablename__ = "sub_tiers"
    __table_args__ = (
        UniqueConstraint(
            "title", "user_id",
            name="uq__sub_tier__title__user_id",
        ),
        UniqueConstraint(
            "price", "user_id",
            name="uq__tier__price__user_id",
        ),
    )

    title: Mapped[str] = mapped_column(String(64))
    text: Mapped[str] = mapped_column(String(256))
    image_url: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
