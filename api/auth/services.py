from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from . import utils as auth_utils
from .access_token import utils as token_utils
from .access_token.repositories import AccessTokenRepo
from api.users import schemas as user_schemas
from api.users.repositories import UserRepo
from core.database import db
from core.settings import settings
from notifications import mail


if TYPE_CHECKING:
    from core.models import User


class AuthService:
    def __init__(
        self,
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
        token_repo: Annotated[AccessTokenRepo, Depends(AccessTokenRepo)],
        session: Annotated[AsyncSession, Depends(db.get_async_session)],
    ) -> None:
        self.user_repo: UserRepo = user_repo
        self.token_repo: AccessTokenRepo = token_repo
        self.session: AsyncSession = session

    async def create_user(self,
                          user: user_schemas.UserCreate) -> "User":
        """
        Crete new user.

        Raise `http_400_bad_request` exception if user with provided
        `useername` or `email` already exists.
        """
        try:
            user_dict = auth_utils.user_dict_hash_password(user.model_dump())
            return await self.user_repo.create(user_dict, self.session)

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
        Get user by username and password (with token),
        raise `http_401_unauthorized` exception if user does't exist.
        """
        user_dict = auth_utils.user_dict_hash_password(user.model_dump())
        validated_user = await self.user_repo.get_one_with_token(
            filters=user_dict,
            session=self.session,
        )
        if validated_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password!",
            )
        return validated_user

    async def get_access_and_refresh_tokens_for_user(
        self,
        user: user_schemas.UserLogin
    ) -> dict[str, str]:
        """
        Create and return `dict` with access and refresh tokens
        for validated user. If refresh token already exists, return it instead.

        Refresh token is stored in database.
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
                session=self.session,
            )
        return tokens

    async def change_user_password(
        self,
        user: "User",
        new_password: str,
        old_password: str | None = None,
    ) -> None:
        """
        Set a new password (hashed) for a user.

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
            filters={"user_id": user.id},
            session=self.session,
        )

    async def get_and_send_reset_token_for_user(self, username: str) -> None:
        """
        Get user by provided username.
        Generate and send reset_token to user's email.

        Raise `http_400_bad_request` if user with such username doesn't exist.
        """
        user = await self.user_repo.get_one(
            filters={"username": username},
            session=self.session,
        )
        if user is None:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with such username doesn't exist.",
            )
        reset_token = token_utils.create_reset_token(username)
        await mail.send_reset_token(user.email, reset_token)

    async def delete_refresh_token(self, user: "User") -> None:
        """Delete user's refresh token."""
        await self.token_repo.delete(
            filters={"user_id": user.id},
            session=self.session,
        )

    @staticmethod
    async def get_user_by_token(
        token: str,
        expected_type: str,
        user_repo: UserRepo,
        session: AsyncSession,
    ) -> "User":
        """
        ** Static method **

        Get session user by provided token,
        raise `http_401_unauthorized` exception if token has
        unexpected type or is invalid.
        """
        validated_token = token_utils.get_token_payload(token)
        token_type = validated_token.get("type")
        if token_type != expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=(f"Invalid token type: {token_type}! "
                        f"Expected: {expected_type}.")
            )
        return await user_repo.get_one(
            filters={"username": validated_token.get("sub")},
            session=session
        )

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(settings.auth.oauth2_scheme)],
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
        session: Annotated[AsyncSession, Depends(db.get_async_session)],
    ) -> "User":
        """
        ** Static method **

        Get current session user by provided `access_token`.

        ** Warning! **

        If this method is injected by `Depends()` into a route function,
        only `authenticated` users will be allowed to use it.
        """
        return await AuthService.get_user_by_token(
            token=token,
            expected_type="access",
            user_repo=user_repo,
            session=session,
        )

    @staticmethod
    async def get_user_by_reset_token(
        token: Annotated[str, Depends(settings.auth.oauth2_scheme)],
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
        session: Annotated[AsyncSession, Depends(db.get_async_session)],
    ) -> "User":
        """
        ** Static method **

        Get current session user by provided `reset_token`.

        ** Warning! **

        If this method is injected by `Depends()` into a route function,
        only users authenticated by reset_token will be allowed to use it.
        Reset token is used only for password reset and has short lifetime.
        """
        return await AuthService.get_user_by_token(
            token=token,
            expected_type="reset",
            user_repo=user_repo,
            session=session,
        )
