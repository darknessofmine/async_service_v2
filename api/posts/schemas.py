from datetime import datetime

from pydantic import BaseModel

from api.comments.schemas import CommentResponse


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
    id: int
    user_id: int
    title: str
    text: str | None = None
    file_url: str | None = None
    sub_tier_id: int | None = None
    created: datetime
    updated: datetime | None = None
    comments: list[CommentResponse]


class PostUpdateResponse(BaseModel):
    id: int
    user_id: int
    title: str
    text: str | None = None
    file_url: str | None = None
    sub_tier_id: int | None = None
    created: datetime
    updated: datetime | None = None
