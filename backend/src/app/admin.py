from fastapi import FastAPI
from sqladmin import Admin, ModelView

from app.core.database import sessionmanager
from models import User, Admin as AdminModel
from utils.admin_auth_backend import authentication_backend
from utils.password import get_hashed_password


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]

    async def on_model_change(self, form, model, is_created, request):
        if is_created:
            form["password"] = get_hashed_password(form["password"])


class AdminAdmin(ModelView, model=AdminModel):
    column_list = [AdminModel.id, AdminModel.email, AdminModel.login]

    async def on_model_change(self, form, model, is_created, request):
        if is_created:
            form["password"] = get_hashed_password(form["password"])


def create_admin_pannel(app: FastAPI) -> Admin:
    admin = Admin(
        app=app,
        engine=sessionmanager._engine,
        authentication_backend=authentication_backend,
    )
    admin.add_view(UserAdmin)
    admin.add_view(AdminAdmin)
