from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import sessionmanager
from app.admin import create_admin_pannel
from routers import include_routes


def init_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """
        Function that handles startup and shutdown events.
        To understand more, read https://fastapi.tiangolo.com/advanced/events/
        """
        yield
        if sessionmanager._engine is not None:
            # Close the DB connection
            await sessionmanager.close()

    # Ініціалізація застосунку FastAPI
    _app = FastAPI(lifespan=lifespan, title=settings.PROJECT_NAME, docs_url="/api/docs")

    # Налаштування CORS
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Підключення усіх роутів
    include_routes(_app)

    return _app


app = init_app()

admin = create_admin_pannel(app=app)
