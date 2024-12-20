from fastapi_users.db import SQLAlchemyBaseUserTable

from .base import Base
from .mixins import IdIntPkMixin


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[int]):
    ...
