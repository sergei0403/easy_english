from sqlalchemy import select, update, delete, insert

from app.core.database import db
from schemas.auth_schemas import RegisterSchema
from models import User


class VocabularyDBService():
    def __init__(self) -> None:
        self.__db_session = db

    async def get_user_by_email(self, email: str) -> User:
        query = await self.__db_session.execute(
            select(User).where(User.email == email)
        )
        return query.scalars().first()

    async def create_vocabulary(self, user_item: RegisterSchema) -> None:
        await self.__db_session.execute(
            insert(User).values(
                email=user_item.email,
                login=user_item.login,
                password=user_item.password,
                first_name=user_item.first_name,
                last_name=user_item.last_name
            )
        )
        await db.commit()
