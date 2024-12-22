from api.utils.repositories import CreateRepo, DeleteRepo

from core.models import AccessToken


class AccessTokenRepo(CreateRepo, DeleteRepo):
    model = AccessToken
