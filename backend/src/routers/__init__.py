from routers.auth_router import auth_router
from routers.vocabularies import vocabulary_router


def include_routes(app):
    app.include_router(auth_router)
    app.include_router(vocabulary_router)
