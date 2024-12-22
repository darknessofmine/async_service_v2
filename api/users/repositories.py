from api.utils.repositories import CreateRepo, GetOneRepo, DeleteRepo

from core.models import User


class UserRepo(CreateRepo, GetOneRepo, DeleteRepo):
    model = User
