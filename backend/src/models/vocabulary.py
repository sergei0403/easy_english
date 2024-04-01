from sqlalchemy import String, Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class Vocabulary(Base):
    __tablename__ = 'vocabularies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("models.users.User", back_populates="vocabularies")


class Words(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True, index=True)
    english_phrase = Column(String(225))
    slug = Column(String(255), index=True)
    translations_list = Column(JSON)
