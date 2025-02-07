from api.utils.repositories import CreateRepo, DeleteRepo
from core.models import Follow


class FollowRepo(CreateRepo[Follow],
                 DeleteRepo[Follow]):
    model = Follow
