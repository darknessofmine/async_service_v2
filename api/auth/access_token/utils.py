from datetime import datetime, timedelta, timezone
from typing import Any, TYPE_CHECKING

import jwt
from fastapi import HTTPException, status

from core.settings import settings


if TYPE_CHECKING:
    from core.models import User


def jwt_encode(
    payload: dict[str, Any],
    private_key: str = settings.auth.jwt.private_key.read_text(),
    algorithm: str = settings.auth.jwt.algorithm,
    expire_minutes: int = settings.auth.jwt.access_token_expire_minutes,
    expire_days: int | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_days is not None:
        expire = now + timedelta(days=expire_days)
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire)
    return jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm,
    )


def jwt_decode(
    token: str,
    public_key: str = settings.auth.jwt.public_key.read_text(),
    algorithm: str = settings.auth.jwt.algorithm,
) -> dict[str, Any]:
    return jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm],
    )


def create_jwt_token(
     token_data: dict,
     token_type: str,
     expire_minutes: int | None = None,
     expire_days: int | None = None,
) -> str:
    jwt_payload = {"type": token_type}
    jwt_payload.update(token_data)
    return jwt_encode(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_days=expire_days,
    )


def create_access_token(user: "User") -> str:
    token_data = {
        "sub": user.username,
        "id": user.id
    }
    return create_jwt_token(
        token_data=token_data,
        token_type="access",
        expire_minutes=settings.auth.jwt.access_token_expire_minutes,
    )


def create_refresh_token(user: "User") -> str:
    token_data = {"sub": user.username}
    return create_jwt_token(
        token_data=token_data,
        token_type="refresh",
        expire_minutes=settings.auth.jwt.refresh_token_expire_days,
    )


def create_reset_token(username: str) -> str:
    token_data = {"sub": username}
    return create_jwt_token(
        token_data=token_data,
        token_type="reset",
        expire_minutes=settings.auth.jwt.reset_password_expire_minutes
    )


def get_token_payload(token: str) -> dict[str, Any]:
    try:
        return jwt_decode(token)
    except jwt.exceptions.InvalidTokenError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token! {error}",
        )
