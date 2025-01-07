from api.utils.repositories import (
    CreateRepo,
    GetOneRepo,
    UpdateRepo,
    DeleteRepo,
)
from core.models import Post


class PostRepo(CreateRepo[Post],
               GetOneRepo[Post],
               UpdateRepo[Post],
               DeleteRepo[Post]):
    model = Post
