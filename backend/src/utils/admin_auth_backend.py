from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select

from app.core.config import settings
from app.core.database import sessionmanager
from models import Admin as AdminModel
from utils.password import verify_password
from utils.jwt_token import generate_token


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        login, password = form["username"], form["password"]

        # Валідація username та password
        async with sessionmanager.session() as db:
            query = await db.execute(
                select(AdminModel).where(AdminModel.login == login)
            )
            admin = query.scalars().first()
        if not admin or not verify_password(
            password=password, hashed_pass=admin.password
        ):
            return False

        # Генерація токену
        date_exp = (
            datetime.now() + timedelta(seconds=settings.ADMIN_TOKEN_EXPIRE_MINUTES)
        ).timestamp()
        token_data = {
            "user_id": admin.id,
            "email": admin.email,
            "date_exp": date_exp,
            "jti": uuid4().hex,
            "token_type": "admin_token",
        }
        # Збереження токену в сесію користувача
        request.session.update({"token": generate_token(token_data=token_data)})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        # Перевірка існування токену
        if not token:
            return False
        return True


authentication_backend = AdminAuth(secret_key="secret")
