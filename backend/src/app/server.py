from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import db
from app.admin import create_admin_pannel
from routers import include_routes


def init_app():
    # Ініціалізація бази данних
    db.init()

    # Ініціалізація застосунку FastAPI
    _app = FastAPI(title=settings.PROJECT_NAME)

    # Lifespan event handler for startup
    async def startup_event():
        # Create database connections, etc.
        await db.create_all()

    _app.add_event_handler("startup", startup_event)

    # Lifespan event handler for shutdown
    async def shutdown_event():
        # Close database connections, etc.
        await db.close()

    _app.add_event_handler("shutdown", shutdown_event)

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
