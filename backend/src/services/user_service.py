from sqlalchemy import select, delete, insert  # update,

from app.core.database import db
from schemas.auth_schemas import RegisterSchema
from models import User


class UserDBService:
    def __init__(self) -> None:
        self.__db_session = db
        print("*" * 100)
        print(self.__db_session._engine)

    async def get_user_by_email(self, email: str) -> User:
        query = await self.__db_session.execute(select(User).where(User.email == email))

        return query.scalars().first()

    async def create_user(self, user_item: RegisterSchema) -> None:
        await self.__db_session.execute(
            insert(User).values(
                email=user_item.email,
                login=user_item.login,
                password=user_item.password,
                first_name=user_item.first_name,
                last_name=user_item.last_name,
            )
        )
        await self.__db_session.commit()

    async def delete_user_by_email(self, email: str) -> None:
        await self.__db_session.execute(
            delete(User).where(
                User.email == email,
            )
        )
        await self.__db_session.commit()
