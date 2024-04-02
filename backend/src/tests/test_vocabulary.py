import pytest

from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from fastapi.testclient import TestClient

from httpx import AsyncClient

from app.server import app
from app.core.database import get_db_session
from models import Base
from utils.utils_for_test import create_test_user, generate_test_token, remove_test_user

client = TestClient(app)

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


@pytest.mark.asyncio
async def test_user_vocabularies():
    await setup()
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as ac:
        async with TestSessionLocal() as db:
            user = await create_test_user(db=db)
            access_token = await generate_test_token(user=user)
            headers = {"Authorization": str(f"Bearer {access_token}")}
            response = await ac.get("/vocabularies/user_vocabulary/", headers=headers)
            await remove_test_user(db=db, email=user.email)
        assert response.status_code == 200
    await teardown()
