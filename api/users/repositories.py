from api.utils.repositories import (
    CreateRepo,
    GetOneRepo,
    DeleteRepo,
    UpdateRepo,
)
from core.models import User


class UserRepo(CreateRepo[User],
               GetOneRepo[User],
               UpdateRepo[User],
               DeleteRepo[User]):
    model = User
