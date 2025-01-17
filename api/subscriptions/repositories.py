from api.utils.repositories import (
    CreateRepo,
    DeleteRepo,
    GetOneRepo,
    UpdateRepo,
)
from core.models import Subscription


class SubsciptionRepo(CreateRepo[Subscription],
                      GetOneRepo[Subscription],
                      UpdateRepo[Subscription],
                      DeleteRepo[Subscription]):
    model = Subscription
