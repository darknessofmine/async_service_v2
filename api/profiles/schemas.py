from pydantic import BaseModel


class ProfileResponse(BaseModel):
    first_name: str
    last_name: str | None = None
    bio: str | None = None


class ProfileUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
