import logging
import os
import uuid
from typing import Generator

import dotenv
import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from alembic.command import downgrade as alembic_downgrade
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from service.__main__ import get_app
from service.config import get_settings
from service.db.connection import get_session

logging.getLogger("faker").setLevel(logging.ERROR)
dotenv.load_dotenv()


class DBManager:
    os.environ["DATABASE_NAME"] = "test_db"  # "test1" # f"pytest-{uuid.uuid4().hex}"
    # os.environ["DATABASE_PORT"] = "5435"
    uri_test = get_settings().sync_database_uri
    if not database_exists(uri_test):
        create_database(uri_test)

    alembic_config = AlembicConfig(file_="alembic_s.ini")
    try:
        alembic_downgrade(alembic_config, "base")
    except Exception as exc:
        ...

    alembic_config.set_main_option("sqlalchemy.url", uri_test)
    alembic_upgrade(alembic_config, "head")
    # yield
    # alembic_downgrade(alembic_config, "base")

    engine = sqlalchemy.create_engine(uri_test, echo=True, future=True)
    session_maker = sessionmaker(engine, expire_on_commit=False, autoflush=False)


def get_session() -> Generator:
    with DBManager.session_maker() as session:
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


# Fixture for database connection.
@pytest.fixture(name="db", scope="session")
def fixture_db():
    try:
        yield next(get_session())
    except StopIteration:
        ...


# Fixture for test client.
@pytest.fixture(name="client", scope="session")
def fixture_client():
    app = get_app()
    with TestClient(app) as client:
        yield client
