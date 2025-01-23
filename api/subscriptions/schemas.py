from pydantic import BaseModel


class SubscriptionResponse(BaseModel):
    owner_id: int
    sub_id: int
    sub_tier_id: int
