import datetime
import json

from abc import ABC
from uuid import uuid4
from pydantic import BaseModel


from app.core.config import settings
from managers.redis_manager import RedisConnection
from utils.jwt_token import generate_token, decode_token, generate_token_data
from models import User
from services.user_service import UserDBService

class UserSchema(BaseModel):
    id: int
    email: str


class TokennRedisModel():
    user_id: int
    jti: str
    access: str
    refresh: str
    created_at: datetime.datetime

    def __init__(self, user_id: int, jti: str, access: str, refresh: str) -> None:
        self.user_id = user_id
        self.jti = jti
        self.access = access
        self.refresh = refresh
        self.created_at = datetime.datetime.now()

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "jti": self.jti,
            "access": self.access,
            "refresh": self.refresh
        }


class BaseStoreToken(ABC):

    def create(self, user: User) -> dict:
        """Create token for user

        Args:
            user (User): User model instance

        Returns:
            dict: includes fields which added in settings.RESPONSE_FIELDS
        """
        raise NotImplementedError

    def get(self, jti: str) -> dict:
        """Return user tokens dict with this token

        Args:
            jti (str): unique string for each token

        Returns:
            dict: includes fields which added in settings.RESPONSE_FIELDS
        """
        raise NotImplementedError

    def update(self, jti: str) -> dict:
        """Update user access token dict with this jti

        Args:
            jti (str): unique string for each token

        Returns:
            dict: includes fields which added in settings.RESPONSE_FIELDS
        """
        raise NotImplementedError

    def delete(self, jti: str) -> None:
        """Delete user token whith this jti

        Args:
            jti (str): unique string for each token
        """
        raise NotImplementedError


class StoreTokenRedis(BaseStoreToken):

    def create(self, user: User) -> dict:
        jti = uuid4().hex
        if isinstance(user, dict):
            user = UserSchema.parse_obj(user)
        else:
            user = UserSchema(**user.__dict__)
        token_data = generate_token_data(
            user=user, jti=jti, live_time=settings.ACCESS_TOKEN_EXPIRE_MINUTES, token_type="access")
        access_token = generate_token(token_data=token_data)
        token_data = generate_token_data(
            user=user, jti=jti, live_time=settings.REFRESH_TOKEN_EXPIRE_MINUTES, token_type="refresh")
        refresh_token = generate_token(token_data=token_data)
        token = TokennRedisModel(user_id=user.id, jti=jti, access=access_token, refresh=refresh_token)
        with RedisConnection(redis_url=settings.REDIS_URL) as redis_client:
            redis_client.set(jti, json.dumps(token.to_dict()))
            # Додаємо видалення зміної jti коли вийде час житя refresh токена
            redis_client.expire(jti, settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        return (token, user)

    async def get(self, jti: str) -> dict:
        with RedisConnection(redis_url=settings.REDIS_URL) as redis_client:
            token = TokennRedisModel(**json.loads(redis_client.get(jti)))
            decoded_token = decode_token(token.refresh)
            user_db_service = UserDBService()
            user = await user_db_service.get_user_by_email(email=decoded_token.get("email"))
        return (token, user)

    async def update(self, jti: str) -> dict:
        with RedisConnection(redis_url=settings.REDIS_URL) as redis_client:
            token = TokennRedisModel(**json.loads(redis_client.get(jti)))
            decoded_token = decode_token(token.refresh)
            user_db_service = UserDBService()
            user = await user_db_service.get_user_by_email(email=decoded_token.get("email"))
            token_data = generate_token_data(
                user=user, jti=jti, live_time=settings.ACCESS_TOKEN_EXPIRE_MINUTES, token_type="access")
            token.access = generate_token(token_data)
            if settings.ROTATE_REFRESH_TOKEN:
                token_data = generate_token_data(
                    user=user, jti=jti, live_time=settings.REFRESH_TOKEN_EXPIRE_MINUTES, token_type="refresh")
                token.refresh = generate_token(token_data)
            redis_client.set(jti, json.dumps(token.to_dict()))
            # Додаємо видалення зміної jti коли вийде час житя refresh токена
            redis_client.expire(jti, settings.REFRESH_TOKEN_EXPIRE_MINUTES) 
        return (token, user)

    def delete(self, jti: str) -> None:
        with RedisConnection(redis_url=settings.REDIS_URL) as redis_client:
            redis_client.delete(jti)
