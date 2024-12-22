from pydantic import BaseModel


class AccessToken(BaseModel):
    token: str
