from fastapi.testclient import TestClient
import pytest
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from service.__main__ import app
from service.config import get_settings


@pytest.fixture(name="client", scope="function")
def fixture_client():
    return TestClient(app)


class TestSess:
    def __init__(self) -> None:
        settings = get_settings()
        engine = sqlalchemy.create_engine(settings.sync_database_uri)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_sess(self):
        return self.session


# Fixture for database connection.
@pytest.fixture(name="db", scope="function")
def fixture_db():
    yield TestSess().get_sess()
