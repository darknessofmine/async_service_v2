from api.utils.repositories import (
    CreateRepo,
    GetOneRepo,
    GetOneWithRelatedListRepo,
    GetOneWithRelatedObjRepo,
    GetOneWithRelatedObjIdRepo,
    DeleteRepo,
    UpdateRepo,
)
from core.models import User


class UserRepo(CreateRepo[User],
               GetOneRepo[User],
               UpdateRepo[User],
               DeleteRepo[User],
               GetOneWithRelatedObjRepo[User],
               GetOneWithRelatedListRepo[User],
               GetOneWithRelatedObjIdRepo[User]):
    model = User
