from sqlalchemy.ext.asyncio import AsyncSession

from db_repositories.vocabulary_repository import VocabularyRepository

from schemas.vocabularies import (
    CreateVocabularySchema,
    FullCreateVocabularySchema,
)
from models import Vocabulary


class VocabularyDBService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.__db_session = db_session
        self.__repository = VocabularyRepository(
            model=Vocabulary, db_session=self.__db_session
        )

    async def create_vocabulary(self, item: dict) -> Vocabulary:
        item = FullCreateVocabularySchema(
            name=item.get("name"), user_id=item.get("user_id")
        ).model_dump()
        vocabulary = await self.__repository.create(obj_in=item)
        return vocabulary

    async def update_vocabulary(
        self, item: CreateVocabularySchema, vocabulary_id: int
    ) -> Vocabulary:
        data = item.model_dump()
        vocabulary = await self.__repository.update_by_id(id=vocabulary_id, obj_in=data)
        return vocabulary

    async def get_user_vocabularies(self, user_id: int) -> list[Vocabulary]:
        return await self.__repository.get_user_vocabularies(user_id=user_id)

    async def delete_vocabularies_by_id(self, id: int) -> None:
        await self.__repository.remove(id=id)
