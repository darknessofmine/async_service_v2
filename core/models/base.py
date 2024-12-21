from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True

    def __repr__(self) -> str:
        if hasattr(self, id):
            return f"<{self.__class__.__name__}: id={self.id}>"

        first_column = self.__table__.columns.keys()[0]
        return (
            f"<{self.__class__.__name__}: "
            f"{first_column}={getattr(self, first_column)}>"
        )
