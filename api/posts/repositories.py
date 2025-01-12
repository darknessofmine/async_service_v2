from api.utils.repositories import (
    CreateRepo,
    GetOneRepo,
    GetOneWithRelatedListRepo,
    UpdateRepo,
    DeleteRepo,
)
from core.models import Post


class PostRepo(CreateRepo[Post],
               GetOneRepo[Post],
               UpdateRepo[Post],
               DeleteRepo[Post],
               GetOneWithRelatedListRepo[Post]):
    model = Post
