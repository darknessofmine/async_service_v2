from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException, status

from .services import AuthService


if TYPE_CHECKING:
    from core.models import User


class Permissions:
    """
    Get current session user and check if any of their roles
    matches required ones.

    - Return current session user on the first match.
    - Raise `http_403_forbidden` exception, if there were no matches.

    Usage:
        Put into dependency with list of required permissions
        (for roles info check `core.models.user: User`)
        ```
        @router.get(
            "/any",
            dependencies=Depends(Permissions(["is_admin"])),
        )
        async def get_any():
            ...

        @router.get("/any")
        async def get_any(
            user: User = Depends(Permissions(["is_admin", "is_verified"])),
        ):
            ...
        ```
    """
    def __init__(self, required_permissions: list[str]) -> None:
        self.required_permissions = required_permissions

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
