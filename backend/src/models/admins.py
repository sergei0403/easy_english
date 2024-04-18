from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Admin(Base):
    __tablename__ = "admins_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    login: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str]

    def __repr__(self) -> str:
        return f"<Admin id={self.id} email={self.email}>"

    def __str__(self) -> str:
        return self.__repr__()
