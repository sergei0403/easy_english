from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), index=True)
    login = Column(String(20))
    password = Column(String(255))
    first_name = Column(String)
    last_name = Column(String)

    vocabularies = relationship("models.vocabulary.Vocabulary", back_populates="user")

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"

    def __str__(self) -> str:
        return self.__repr__()
