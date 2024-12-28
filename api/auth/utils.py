import hashlib
from typing import Any

from core.settings import settings


def hash_password(password: str) -> str:
    encoded_password = (password + settings.auth.salt).encode("utf-8")
    return hashlib.sha512(encoded_password).hexdigest()


def user_dict_hash_password(user_dict: dict[str, Any]) -> dict[str, Any]:
    hashed_password = hash_password(user_dict.get("password"))
    user_dict["password"] = hashed_password
    return user_dict


def is_password_same(current: str, provided: str) -> bool:
    return current == hash_password(provided)


def get_verification_url(token: str) -> str:
    return f"{settings.app.domain}/auth/verification/{token}"
