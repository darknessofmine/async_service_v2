from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin


if TYPE_CHECKING:
    from core.models import User


class Follow(Base, IntIdPkMixin):
    __tablename__ = "follows"
    __table_args__ = (
        UniqueConstraint(
            "owner_id", "client_id",
            name="uq__follow__owner_id__client_id"
        ),
    )

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(
        back_populates="follows",
        foreign_keys="Follow.owner_id",
    )
    client: Mapped["User"] = relationship(
        back_populates="followers",
        foreign_keys="Follow.client_id",
    )
