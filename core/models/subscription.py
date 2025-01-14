from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin


if TYPE_CHECKING:
    from core.models import SubTier, User


class Subscription(Base, IntIdPkMixin):
    __tablename__ = "subscriptions"
    __table_args__ = (
        UniqueConstraint(
            "owner_id", "sub_id",
            name="uq__subscription__owner_id__sub_id"
        ),
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    sub_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    sub_tier_id: Mapped[int] = mapped_column(
        ForeignKey("sub_tiers.id", ondelete="SET NULL")
    )

    owner: Mapped["User"] = relationship(
        back_populates="subscriptions",
        foreign_keys="Subscription.owner_id",
    )
    sub: Mapped["User"] = relationship(
        back_populates="subscribers",
        foreign_keys="Subscription.sub_id",
    )
    sub_tier: Mapped["SubTier"] = relationship(back_populates="subscriptions")
