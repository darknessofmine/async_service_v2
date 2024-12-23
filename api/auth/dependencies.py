from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .service import AuthService
from api.auth.access_token.repositories import AccessTokenRepo
from api.users.repositories import UserRepo
from core.database import db


async def get_auth_service(
    session: Annotated[AsyncSession, Depends(db.get_async_session)],
) -> AuthService:
    return AuthService(AccessTokenRepo, UserRepo, session=session)
