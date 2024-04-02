from schemas.auth_schemas import RegisterSchema
from services.user_service import UserDBService
from storages.jwt_token_storage import StoreTokenRedis


async def create_test_user(db):
    data = {
        "email": "example@example.com",
        "login": "example",
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123",
        "r_password": "password123",
    }

    # Create an instance of RegisterSchema from the dictionary
    user_item = RegisterSchema.parse_obj(data)
    user_service = UserDBService(db)
    user = await user_service.get_user_by_email(email=user_item.email)
    if not user:
        await user_service.create_user(user_item=user_item)
        user = await user_service.get_user_by_email(email=user_item.email)
    return user


async def remove_test_user(db, email: str) -> None:
    user_service = UserDBService(db)
    await user_service.delete_user_by_email(email=email)


async def generate_test_token(user) -> str:
    token_storage = StoreTokenRedis()
    token, _ = token_storage.create(user=user)
    return token.access
