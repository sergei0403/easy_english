import pytest

from unittest.mock import patch
from fastapi.testclient import TestClient

from httpx import AsyncClient

from app.server import app
from tests.utils_for_test import create_test_user, generate_test_token, remove_test_user

client = TestClient(app)


@pytest.mark.asyncio
async def test_read_main():
    # mock_user = {
    #     "id": 1,
    #     "email": "example@example.com",
    #     "login": "example",
    #     "first_name": "John",
    #     "last_name": "Doe",
    #     "password": "password123",
    #     "r_password": "password123"
    # }  # Mock user data

    # with patch("services.user_service.UserDBService.create_user") as mock_create_user:
    #     mock_create_user.return_value = mock_user
    #     async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as ac:
    #         # user = await create_test_user()
    #         access_token = await generate_test_token(user=mock_user)
    #         headers = {"Authorization": str(f"Bearer {access_token}")}
    #         response = await ac.get("/vocabularies/", headers=headers)
    #         # await remove_test_user(email=user.email)
    #         assert response.status_code == 200
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as ac:
        user = await create_test_user()
        access_token = await generate_test_token(user=user)
        headers = {"Authorization": str(f"Bearer {access_token}")}
        response = await ac.get("/vocabularies/user_vocabulary/", headers=headers)
        await remove_test_user(email=user.email)
        assert response.status_code == 200
