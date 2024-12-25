from api.utils.repositories import CreateRepo, DeleteRepo
from core.models import AccessToken


class AccessTokenRepo(CreateRepo[AccessToken],
                      DeleteRepo[AccessToken]):
    model = AccessToken
