from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: id={self.id}>"
