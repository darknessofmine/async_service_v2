from pydantic import BaseModel, Field


class AccessTokenInfo(BaseModel):
    access_token: str = Field(validation_alias="token")
    token_type: str = "Bearer"
