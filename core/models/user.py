from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IntIdPkMixin


class User(Base, IntIdPkMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        index=True
    )
    password: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(256), unique=True)
    is_active: Mapped[bool] = mapped_column(server_default=True)
    is_superuser: Mapped[bool] = mapped_column(server_default=False)
