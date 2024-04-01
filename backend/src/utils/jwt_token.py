import jwt
from jwt.exceptions import DecodeError
from datetime import datetime, timedelta

from app.core.config import settings
from models import User


def generate_token_data(user: User, jti: str, live_time: int, token_type: str) -> dict:
    date_exp = (datetime.now() + timedelta(seconds=live_time)).timestamp()
    return {
        "user_id": user.id,
        "email": user.email,
        "date_exp": date_exp,
        "jti": jti,
        "token_type": token_type,
    }


def generate_token(token_data: dict) -> str:
    """Кодуємо токен на основі переданих параметрів"""
    token = jwt.encode(token_data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_token(token: str) -> dict:
    """Декодуємо отриманий токен"""
    try:
        decoded_token = jwt.decode(
            token, settings.JWT_SECRET_KEY, options={"verify_signature": False}
        )
    except DecodeError:
        return None
    return decoded_token


def check_expired_token(timestamp: int) -> bool:
    """Перевіряємо чи токен активний"""
    date_time_obj = datetime.fromtimestamp(int(timestamp))
    now = datetime.now()
    condition = date_time_obj < now
    return True if date_time_obj > now else False
