from sqlalchemy.ext.asyncio import AsyncSession

from db_repositories.user_repository import UserRepository
from schemas.auth_schemas import RegisterSchema
from models import User


class UserDBService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.__db_session = db_session
        self.__repository = UserRepository(model=User, db_session=self.__db_session)

    async def get_user_by_email(self, email: str) -> User:
        user = await self.__repository.get_user_by_email(email=email)
        return user

    async def create_user(self, user_item: RegisterSchema) -> None:
        insert_data = user_item.model_dump()
        insert_data.pop("r_password")
        print(f"{insert_data=}")
        user = None
        if not await self.get_user_by_email(email=insert_data.get("email")):
            user = await self.__repository.create(obj_in=insert_data)
        return user

    async def delete_user_by_email(self, email: str) -> None:
        await self.__repository.delete_user_by_email(email=email)
