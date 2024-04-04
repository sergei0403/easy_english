from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.server import app
from app.core.database import get_db_session
from models import Base
from schemas.auth_schemas import RegisterSchema
from services.user_service import UserDBService
from storages.jwt_token_storage import StoreTokenRedis


DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

TestSessionLocal = async_sessionmaker(autocommit=False, bind=engine)


async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db_session] = override_get_db


async def setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def teardown():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_test_user():
    data = {
        "email": "example@example.com",
        "login": "example",
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123",
        "r_password": "password123",
    }

    # Create an instance of RegisterSchema from the dictionary
    user_item = RegisterSchema.model_validate(data)
    async with TestSessionLocal() as db:
        user_service = UserDBService(db)
        user = await user_service.get_user_by_email(email=user_item.email)
        if not user:
            await user_service.create_user(user_item=user_item)
            user = await user_service.get_user_by_email(email=user_item.email)
    return user


async def remove_test_user(email: str) -> None:
    async with TestSessionLocal() as db:
        user_service = UserDBService(db)
        await user_service.delete_user_by_email(email=email)


async def generate_test_token(user) -> str:
    token_storage = StoreTokenRedis()
    token, _ = token_storage.create(user=user)
    return token.access
