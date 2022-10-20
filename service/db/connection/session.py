from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from service.config import get_settings


class DBManager:
    @property
    def uri(self):
        async_database_uri = get_settings().database_uri
        return async_database_uri

    @property
    def engine(self):
        engine1 = create_async_engine(self.uri, echo=True, future=True)
        return engine1

    @property
    def session_maker(self):
        session_maker1 = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        return session_maker1


async def get_session() -> AsyncGenerator:
    async with DBManager().session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as exc:
            await session.rollback()
            raise exc
        finally:
            await session.close()


__all__ = ["get_session"]
