from typing import Type
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from db_repositories.base_repository import BaseDBRepository, ModelType


class VocabularyRepository(BaseDBRepository):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        super().__init__(model=model, db_session=db_session)
        self.__db_session = self.get_db()

    async def get_user_vocabularies(self, user_id: int):
        query = await self.__db_session.execute(
            select(self.model)
            .where(self.model.user_id == user_id)
            .options(joinedload(self.model.user))
        )
        return query.scalars().all()
