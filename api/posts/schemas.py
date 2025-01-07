from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    text: str | None = None
    file_url: str | None = None
    sub_tier_id: int | None = None


class PostUpdate(BaseModel):
    title: str | None = None
    text: str | None = None
    file_url: str | None = None
    sub_tier_id: int | None = None


class PostResponse(BaseModel):
    title: str
    text: str | None = None
    file_url: str | None = None
    sub_tier_id: int | None = None
    created: datetime
    updated: datetime | None = None
