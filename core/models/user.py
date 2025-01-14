from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin


if TYPE_CHECKING:
    from core.models import (
        AccessToken,
        Comment,
        Post,
        Profile,
        Subscription,
        SubTier,
    )


class User(Base, IntIdPkMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        index=True
    )
    password: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String(256), unique=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_author: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    token: Mapped[Optional["AccessToken"]] = relationship()
    profile: Mapped[Optional["Profile"]] = relationship(back_populates="user")
    sub_tiers: Mapped[Optional[list["SubTier"]]] = relationship(
        back_populates="user",
    )
    posts: Mapped[Optional[list["Post"]]] = relationship(back_populates="user")
    comments: Mapped[Optional[list["Comment"]]] = relationship(
        back_populates="user",
    )
    subscriptions: Mapped[Optional[list["Subscription"]]] = relationship(
        back_populates="owner",
        foreign_keys="Subscription.sub_id",
    )
    subscribers: Mapped[Optional[list["Subscription"]]] = relationship(
        back_populates="sub",
        foreign_keys="Subscription.sub_id",
    )
