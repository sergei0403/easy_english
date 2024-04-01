import os

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl,  ConfigDict, field_validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "easy_words"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = os.environ.get(
        "BACKEND_CORS_ORIGINS",
        [
            "http://localhost:8000",
            "https://localhost:8000",
            "http://localhost",
            "https://localhost",
            "http://0.0.0.0:8080",
            "http://localhost:3000",
        ],
    )
    SERVER_PORT: int = 8000
    SERVER_HOST: str = "0.0.0.0"

    DB_NAME: str = os.environ.get("DB_NAME", "postgres")
    DB_USER: str = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "postgres")
    DB_HOST: str = os.environ.get("DB_HOST", "database")
    DB_PORT: int = int(os.environ.get("DB_PORT", 5432))

    DATABASE_DSN: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://:redispass@redis:6379/0")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", int(60 * 24))  # 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", int(60 * 24 * 7)) # 7 days
    ADMIN_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ADMIN_TOKEN_EXPIRE_MINUTES", int(60 * 24 * 7)) # 7 days
    ROTATE_REFRESH_TOKEN: bool = os.environ.get("ROTATE_REFRESH_TOKEN", False)
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY', 'develop')     # should be kept secret

    class Config(ConfigDict):
        case_sensitive = True
        env_file = ".env"

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
