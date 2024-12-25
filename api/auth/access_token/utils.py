from datetime import datetime, timedelta, timezone
from typing import Any
import uuid

import jwt

from core.settings import settings


def generate_uuid_access_token() -> str:
    return uuid.uuid4()


def jwt_encode(
    payload: dict[str, Any],
    private_key: str = settings.auth.jwt.public_key.read_text(),
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
    token: str | bytes,
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
