from pydantic import BaseModel


class AccessTokenInfo(BaseModel):
    token: str
    token_type: str = "Bearer"
