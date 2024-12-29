from api.utils.repositories import CreateRepo, UpdateRepo
from core.models import Profile


class ProfileRepo(CreateRepo[Profile],
                  UpdateRepo[Profile]):
    model = Profile
