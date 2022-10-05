import pytest
from sqlalchemy import insert, select

from service.db.models import Marks, Movie, User
from service.schemas.marks import MarkSchema

pytestmark = pytest.mark.asyncio

# def test_sample(client):
#     response = client.post(
#         "/api/test/handle",
#         json={
#             "id": 1,
#             "name": "test",
#             "description": "test",
#         },
#     )
#     assert response.status_code == 404

# from service.db.crud import db_insert, db_select, db_update
