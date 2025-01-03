from pydantic import BaseModel


class SubTierCreate(BaseModel):
    title: str
    text: str
    price: int
    image_url: str | None


class SubTierResponse(BaseModel):
    id: int
    title: str
    text: str
    price: int
    image_url: str | None
