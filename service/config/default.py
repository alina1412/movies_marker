from pydantic import BaseSettings
from starlette.config import Config

config = Config(".env")


class DefaultSettings(BaseSettings):
    """Default settings for the service."""

    # Service
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = config("APP_PORT", cast=int)
    API_PREFIX: str = "/api"

    # Logging
    LOG_LEVEL: str = "debug"

    # Database
    DATABASE_NAME: str = config("DATABASE_NAME", cast=str)
    POSTGRES_HOST: str = config("POSTGRES_HOST", default="localhost", cast=str)
    DATABASE_USERNAME: str = config("DATABASE_USERNAME", cast=str)
    POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int)
    DATABASE_PASSWORD: str = config("DATABASE_PASSWORD", cast=str)
    DB_CONNECT_RETRY: int = config("DB_CONNECT_RETRY", default=20, cast=str)
    DB_POOL_SIZE: int = config("DB_POOL_SIZE", default=15, cast=str)

    @property
    def database_uri(self) -> str:
        """Return the database URL."""
        return (
            f"postgresql+asyncpg://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.DATABASE_NAME}"
        )

    @property
    def sync_database_uri(self) -> str:
        """Return the database URL."""
        return (
            f"postgresql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.DATABASE_NAME}"
        )
