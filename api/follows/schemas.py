from pydantic import BaseModel


class FollowResponse(BaseModel):
    id: int
    owner_id: int
    cliend_id: int
