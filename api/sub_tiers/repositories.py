from api.utils.repositories import (
    CreateRepo,
    GetOneRepo,
    GetManyRepo,
    UpdateRepo,
    DeleteRepo,
)
from core.models import SubTier


class SubTierRepo(CreateRepo[SubTier],
                  GetOneRepo[SubTier],
                  GetManyRepo[SubTier],
                  UpdateRepo[SubTier],
                  DeleteRepo[SubTier]):
    model = SubTier
