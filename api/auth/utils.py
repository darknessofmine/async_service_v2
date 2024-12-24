import hashlib
from typing import Any

from core.settings import settings


def get_password_hash_with_salt(password: str) -> str:
    encoded_password = (password + settings.auth.salt).encode("utf-8")
    return hashlib.sha512(encoded_password).hexdigest()


def user_dict_hash_password(user_dict: dict[str, Any]) -> dict[str, Any]:
    hashed_password = get_password_hash_with_salt(user_dict.get("password"))
    user_dict["password"] = hashed_password
    return user_dict
