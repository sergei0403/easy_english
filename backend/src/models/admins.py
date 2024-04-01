from app.core.database import Base
from sqlalchemy import Column, Integer, String


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), index=True)
    login = Column(String(100), index=True)
    password = Column(String(255))

    def __repr__(self) -> str:
        return f"<Admin id={self.id} email={self.email}>"

    def __str__(self) -> str:
        return self.__repr__()
