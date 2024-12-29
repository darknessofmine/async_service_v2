from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin


if TYPE_CHECKING:
    from core.models import User


class Profile(Base, IntIdPkMixin):
    __tablename__ = "profiles"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            name="uq__profile__user_id",
        ),
    )

    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32), nullable=True)
    bio: Mapped[str] = mapped_column(String(500), nullable=True)
    image_url: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )

    user: Mapped["User"] = relationship(back_populates="profile")
