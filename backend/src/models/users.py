from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
import models


class User(Base):
    __tablename__ = "users_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    login: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]

    vocabularies: Mapped[List["models.vocabulary.Vocabulary"]] = relationship(
        back_populates="user"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"

    def __str__(self) -> str:
        return self.__repr__()
