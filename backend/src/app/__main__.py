import uvicorn

from app.core.config import settings

uvicorn.run(
    "app.server:app",
    host=settings.SERVER_HOST,
    port=settings.SERVER_PORT,
    reload=True,
)
