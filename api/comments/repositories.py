from api.utils.repositories import (
    CreateRepo,
    UpdateRepo,
    DeleteRepo,
)

from core.models import Comment


class CommentRepo(CreateRepo[Comment],
                  UpdateRepo[Comment],
                  DeleteRepo[Comment]):

    model = Comment
