from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin


if TYPE_CHECKING:
    from core.models import AccessToken


class User(Base, IntIdPkMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        index=True
    )
    password: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(256), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    token: Mapped["AccessToken"] | None = relationship()
