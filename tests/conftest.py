from typing import Generator
import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from service.__main__ import app
from service.config import get_settings
from service.db.connection import get_session


# Fixture for test client.
@pytest.fixture(name="client", scope="function")
def fixture_client():
    with TestClient(app) as client:
        yield client


class DBManager:
    uri = get_settings().sync_database_uri
    engine = sqlalchemy.create_engine(uri, echo=True, future=True)
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
@pytest.fixture(name="db", scope="function")
def fixture_db():
    try:
        yield next(get_session())
    except StopIteration:
        ...

