import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app
from utils.utils_for_test import (
    create_test_user,
    generate_test_token,
    remove_test_user,
    setup,
    teardown,
)

client = TestClient(app)


@pytest.mark.asyncio
async def test_user_vocabularies():
    await setup()
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as ac:
        user = await create_test_user()
        access_token = await generate_test_token(user=user)
        headers = {"Authorization": str(f"Bearer {access_token}")}
        response = await ac.get("/vocabularies/user_vocabulary/", headers=headers)
        await remove_test_user(email=user.email)
        assert response.status_code == 200
    await teardown()
