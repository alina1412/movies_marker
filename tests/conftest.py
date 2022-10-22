import logging
import os

import dotenv
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from alembic.command import downgrade as alembic_downgrade
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from service.__main__ import app
from service.config.default import DefaultSettings
from service.db.connection.session import DBManager

logging.getLogger("faker").setLevel(logging.ERROR)
dotenv.load_dotenv()


def run_alembic(uri_test):
    alembic_config = AlembicConfig(file_="alembic_as.ini")
    try:
        alembic_downgrade(alembic_config, "base")
    except Exception as exc:
        ...
    alembic_config.set_main_option("sqlalchemy.url", uri_test)
    alembic_upgrade(alembic_config, "head")


@pytest.fixture(name="change_db", scope="session")
def changes_for_test_db():
    os.environ["DATABASE_NAME"] = "pytest1"
    uri_test = DBManager().uri

    sync_uri = DefaultSettings().sync_database_uri
    if not database_exists(sync_uri):
        create_database(sync_uri)
    run_alembic(uri_test)

    yield uri_test
    # alembic_config = AlembicConfig(file_="alembic_as.ini")
    # alembic_downgrade(alembic_config, "base")


@pytest_asyncio.fixture(name="db", scope="function")
async def get_test_session(change_db):
    uri_test = change_db
    engine = create_async_engine(uri_test, echo=True, future=True)
    session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )

    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            await session.close()


# Fixture for test client.
@pytest.fixture(name="client", scope="session")
def fixture_client():
    with TestClient(app) as client:
        yield client
