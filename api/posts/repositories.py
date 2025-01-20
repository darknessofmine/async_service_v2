from api.utils.repositories import (
    CreateRepo,
    GetManyRepo,
    GetOneRepo,
    UpdateRepo,
    DeleteRepo,
)
from core.models import Post


class PostRepo(CreateRepo[Post],
               GetOneRepo[Post],
               GetManyRepo[Post],
               UpdateRepo[Post],
               DeleteRepo[Post]):
    model = Post
