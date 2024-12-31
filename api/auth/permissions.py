from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException, status

from .services import AuthService


if TYPE_CHECKING:
    from core.models import User


class Permissions:
    def __init__(self, required: list[str]) -> None:
        self.required_permissions = required

    def __call__(
        self,
        user: Annotated["User", Depends(AuthService.get_current_user)],
    ) -> "User":
        for permission in self.required_permissions:
            if user.as_dict()[permission]:
                return user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to do this :("
        )
