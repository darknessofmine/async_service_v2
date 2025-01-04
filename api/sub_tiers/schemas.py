from pydantic import BaseModel


class SubTierCreate(BaseModel):
    title: str
    text: str
    price: int
    image_url: str | None = None


class SubTierUpdate(BaseModel):
    title: str | None = None
    text: str | None = None
    price: int | None = None
    image_url: str | None = None


class SubTierResponse(BaseModel):
    id: int
    title: str
    text: str
    price: int
    image_url: str | None = None
