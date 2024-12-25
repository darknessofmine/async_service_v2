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


if TYPE_CHECKING:
    from core.models import AccessToken, User


class AuthService:
    def __init__(
        self,
        token_repo: Annotated[AccessTokenRepo, Depends(AccessTokenRepo)],
        user_repo: Annotated[UserRepo, Depends(UserRepo)],
        session: Annotated[AsyncSession, Depends(db.get_async_session)],
    ) -> None:
        self.token_repo: AccessTokenRepo = token_repo
        self.user_repo: UserRepo = user_repo
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

    async def get_access_token_for_user(
        self,
        user: user_schemas.UserLogin
    ) -> "AccessToken":
        """
        Create and return new token for validated user if it doesn't exist yet,
        otherwise get and return current token.
        """
        validated_user = await self.validate_auth_user(user)
        if validated_user.token is not None:
            return validated_user.token
        token_dict = {
            "token": str(token_utils.generate_uuid_access_token()),
            "user_id": validated_user.id,
        }
        return await self.token_repo.create(token_dict, self.session)

    async def delete_access_token(self, user: "User") -> None:
        """Delete user's access token."""
        await self.token_repo.delete(
            filters={"user_id": user.id},
            session=self.session,
        )

    async def change_user_password(self,
                                   user: "User",
                                   old_password: str,
                                   new_password: str) -> None:
        """
        Set new password (hashed) to a user.

        Raise `http_400_bad_request` exception if provided old_password
        is different from the current one, or if new_password is the same
        as the old one.
        """
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

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(settings.auth.oauth2_scheme)],
        token_repo: Annotated[AccessTokenRepo, Depends(AccessTokenRepo)],
        session: Annotated[AsyncSession, Depends(db.get_async_session)],
    ) -> "User":
        """
        ** Static method **

        Get and return current session user by provided access token,
        raise `http_401_unauthorized` exception if token is invalid or
        hasn't been provided.

        ** Warning! **

        If this method is injected by `Depends()` into a route function,
        only `authenticated` users will be allowed to use it.
        """
        validated_token = await token_repo.get_one_with_user(
            filters={"token": token},
            session=session,
        )
        if validated_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token!",
            )
        return validated_token.user
