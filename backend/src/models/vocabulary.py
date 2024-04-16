from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
import models


class Vocabulary(Base):
    __tablename__ = "vocabularies_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))
    user: Mapped["models.users.User"] = relationship(back_populates="vocabularies")


class Words(Base):
    __tablename__ = "words_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    english_phrase: Mapped[str]
    slug: Mapped[str] = mapped_column(index=True, unique=True)
    translations_list: Mapped[JSON] = mapped_column(type_=JSON, nullable=False)
