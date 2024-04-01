from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings


Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        self._engine = create_async_engine(
            settings.DATABASE_DSN,
            future=True,
            echo=True,
        )
        self._session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


# Update for testing with SQLite
class TestDatabaseSession():
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        self._engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:",
            echo=True,
        )
        self._session = sessionmaker(self._engine, class_=AsyncSession, expire_on_commit=False)()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

if settings.IS_TEST_DATABASE:
    print(f"{settings.IS_TEST_DATABASE=}")
    db = TestDatabaseSession()
else:
    print(f"{settings.IS_TEST_DATABASE=}") 
    db = AsyncDatabaseSession()    
