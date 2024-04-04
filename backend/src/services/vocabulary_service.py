from sqlalchemy import insert

from models import Vocabulary


class VocabularyDBService:
    def __init__(self, db_session) -> None:
        self.__db_session = db_session

    async def create_vocabulary(self, item_dict: dict) -> None:
        await self.__db_session.execute(
            insert(Vocabulary).values(
                name=item_dict.get("name"), user_id=item_dict.get("user_id")
            )
        )
        await self.__db_session.commit()
