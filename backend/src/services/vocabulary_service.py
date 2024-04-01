from sqlalchemy import select, update, delete, insert

from app.core.database import db
from schemas.auth_schemas import RegisterSchema
from models import Vocabulary


class VocabularyDBService:
    def __init__(self) -> None:
        self.__db_session = db

    async def create_vocabulary(self, item_dict: dict) -> None:
        await self.__db_session.execute(
            insert(Vocabulary).values(
                name=item_dict.get("name"), user_id=item_dict.get("user_id")
            )
        )
        await self.__db_session.commit()
