from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from . import utils as auth_utils
from .access_token import utils as token_utils
from .access_token.repositories import AccessTokenRepo
from api.users import schemas as user_schemas
from api.users.repositories import UserRepo
from core.settings import settings
from core.models import User


class AuthService:
    def __init__(
        self,
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
        token_repo: Annotated[AccessTokenRepo, Depends(AccessTokenRepo)],
    ) -> None:
        self.user_repo: UserRepo = user_repo
        self.token_repo: AccessTokenRepo = token_repo

    async def create_user(self,
                          user: user_schemas.UserCreate) -> "User":
        """
        Create new user.

        Raise `http_400_bad_request` exception if user with provided
        `username` or `email` already exists.
        """
        user_dict = auth_utils.user_dict_hash_password(user.model_dump())
        try:
            return await self.user_repo.create(user_dict)
        except IntegrityError as error:
            orig_detail = error.__dict__["orig"]
            error_field = str(orig_detail).split("\"")[3]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with {error_field} already exists!",
            )

    async def validate_auth_user(self,
                                 user: user_schemas.UserLogin) -> "User":
        """
        Get user by username and password (with token).

        Raise `http_401_unauthorized` exception if user doesn't exist.
        """
        valid_user = await self.user_repo.get_one(
            filters={"username": user.username},
            related_o2o_models=[User.token],
        )
        if not (
            valid_user is not None
            and auth_utils.is_password_same(valid_user.password, user.password)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password!",
            )
        return valid_user

    async def get_access_and_refresh_tokens_for_user(
        self,
        user: user_schemas.UserLogin
    ) -> dict[str, str]:
        """
        Create and return `dict` with access and refresh tokens
        for validated user. If refresh token already exists, return it instead.
        Refresh token is stored in database.

        Raise `http_401_unauthorized` exception if user doesn't exist.
        """
        validated_user = await self.validate_auth_user(user)
        tokens = {
            "access_token": token_utils.create_access_token(validated_user),
            "refresh_token": token_utils.create_refresh_token(validated_user),
        }
        if validated_user.token is None:
            await self.token_repo.create(
                data_dict={
                    "token": tokens["refresh_token"],
                    "user_id": validated_user.id,
                },
            )
        return tokens

    @staticmethod
    def create_verification_url(user: "User") -> str:
        """
        Generate `verification_token` for a user.
        """
        token = token_utils.create_verification_token(user.username)
        return auth_utils.get_verification_url(token=token)

    async def verify_user_by_token(self, token: str) -> None:
        """
        Verify user by `verification_token`.
        """
        validated_token = token_utils.validate_token(token, "verification")
        user = await self.user_repo.get_one(
            filters={"username": validated_token.get("sub")},
        )
        await self.user_repo.update(
            update_dict={"is_verified": True},
            filters={"username": user.username}
        )

    async def change_user_password(
        self,
        user: "User",
        new_password: str,
        old_password: str | None = None,
    ) -> None:
        """
        Set a new hashed password for a user.

        Raise `http_400_bad_request` exception if old_password is provided
        and is different from the current one, or if new_password is the same
        as the current one.
        """
        if old_password is not None:
            if not auth_utils.is_password_same(user.password, old_password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid current password."
                )
        if auth_utils.is_password_same(user.password, new_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password has to be different from the old one."
            )
        new_password_hashed = auth_utils.hash_password(new_password)
        await self.user_repo.update(
            update_dict={"password": new_password_hashed},
            filters={"username": user.username},
        )

    async def get_user_by_username(self, username: str) -> "User":
        """
        Get user by provided username.

        Raise `http_400_bad_request` if user with such username doesn't exist.
        """
        user = await self.user_repo.get_one(
            filters={"username": username},
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with such username doesn't exist.",
            )
        return user

    @staticmethod
    def get_reset_token_for_user(user: "User") -> str:
        """
        Generate reset_token for a user.
        """
        return token_utils.create_reset_token(user.username)

    async def reset_user_password(
        self,
        user: "User",
        passwords: user_schemas.UserPasswordReset,
    ) -> None:
        """
        Set new hashed password for a user.

        Raise `http_400_bad_request` exception if password and
        password repead are different from each other,
        or if new_password is the same as the current one.
        """
        if passwords.new_password != passwords.new_password_repeat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords are not the same."
            )
        await self.change_user_password(user, passwords.new_password)

    async def delete_refresh_token(self, user: "User") -> None:
        """
        Delete user's refresh token.
        """
        await self.token_repo.delete(
            filters={"user_id": user.id},
        )

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(settings.auth.oauth2_scheme)],
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
    ) -> "User":
        """
        ** Static method **

        Get current session user by provided `access_token`.

        ** Warning! **

        If this method is injected by `Depends()` into a route function,
        only `authenticated` users will be allowed to use it.
        """
        validated_token = token_utils.validate_token(token, "access")
        return await user_repo.get_one(
            filters={"username": validated_token.get("sub")},
            related_o2o_models=[User.profile],
        )

    @staticmethod
    async def get_user_by_reset_token(
        token: Annotated[str, Depends(settings.auth.oauth2_scheme)],
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
    ) -> "User":
        """
        ** Static method **

        Get current session user by provided `reset_token`.

        ** Warning! **

        If this method is injected by `Depends()` into a route function,
        only users authenticated by reset_token will be allowed to use it.
        Reset token is used only for password reset and has short lifetime.
        """
        validated_token = token_utils.validate_token(token, "reset")
        return await user_repo.get_one(
            filters={"username": validated_token.get("sub")},
        )
