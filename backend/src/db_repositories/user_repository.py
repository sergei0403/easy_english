from typing import Optional, Type
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db_repositories.base_repository import BaseDBRepository, ModelType


class UserRepository(BaseDBRepository):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        super().__init__(model=model, db_session=db_session)
        self.__db_session = self.get_db()

    async def get_user_by_email(self, email: str) -> Optional[ModelType]:
        query = await self.__db_session.execute(
            select(self.model).where(self.model.email == email)
        )
        return query.scalars().first()

    async def delete_user_by_email(self, email: str) -> None:
        await self.__db_session.execute(
            delete(self.model).where(
                self.model.email == email,
            )
        )
        await self.__db_session.commit()
