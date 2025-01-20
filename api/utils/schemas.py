from typing import Any

from pydantic import BaseModel


class PropertyFilter(BaseModel):
    """
    ** WARNING

    `related_model` must be of the same instance it's being used with.

    Usage example:
        ```
        post_reporisory.get_many(
            ...
            prop_filter = PropertyFilter(
                related_model=Post.user,
                model_field=User.username,
                field_value=username,
            )
            ...
        )
        ```
    """

    related_model: Any
    model_field: Any
    field_value: Any
