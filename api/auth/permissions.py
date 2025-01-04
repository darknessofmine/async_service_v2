from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from .access_token import utils as token_utils
from .services import AuthService
from api.users.repositories import UserRepo
from core.settings import settings
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
            dependencies=[Depends(Permissions(["is_admin"]))],
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


class IsOwner:
    """
    Get current session user with required object (`obj_name: obj_id`)

    - Return current session user if user is owner of required object.
    - Raise `http_403_forbidden` exception, if user owns no objects with
      such parameters.

    ** WARNING **
        Using this class you no longer can use path parameter `{any_id}`
        inside your route, since it is being used to get user
        with requred object. You can get access to it via `user` model:
        ```
        post_id = user.posts[0].id # for one-to-many relationship
        profile_id = user.profile.id # for one-to-one relationship
        ```
    Usage:
        Put into dependency with the name of required object:
        ```
        @router.get(
            "/any",
            dependencies=[Depends(IsOwner("post"))],
        )
        async def get_any():
            ...

        @router.get("/any")
        async def get_any(
            user: Annotated[User, Depends(Permissions("comment"))],
        ):
            ...
        ```
    """
    def __init__(self, obj_name: str) -> None:
        self.obj_name = obj_name

    async def __call__(
        self,
        obj_id: Annotated[int, Path],
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
        token: Annotated[str, Depends(settings.auth.oauth2_scheme)],
    ) -> "User":

        validated_token = token_utils.validate_token(token, "access")
        if self.obj_name == "sub_tier":
            user = await AuthService.get_user_by_token(
                token=validated_token,
                repo_method=user_repo.get_one_with_related_obj_id,
                related_model=User.sub_tiers,
                related_model_id=obj_id,
            )

        if user is not None:
            return user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=("You are not allowed to do this :( "
                    "May be it has already been deleted.")
        )
