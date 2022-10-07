import json
import logging

import pytest

from service.db.models import Marks, Movie, User
from service.schemas.marks import MarkSchema
from tests.utils import db_insert, db_select, db_update

logging.getLogger("faker.factory").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# @pytest.mark.my
def test_add_movie(client, db):
    url = "/api/movie/add-movie"
    response = client.post(url + "?title=Title1")
    assert response.status_code == 201
    response = client.post(url + "?title=Title2")
    assert response.status_code == 201


# @pytest.mark.my
def test_add_movie2(client, db):
    url = "/api/movie/add-movie"
    response = client.post(url + "?title=Title3")
    assert response.status_code == 201
    response = client.post(url + "?title=Title4")
    assert response.status_code == 201


def add_or_get_movie_id(session, title) -> int:
    id = db_select(session, (Movie.id,), (Movie.title == title,))
    if not id:
        db_insert(session, Movie, {"title": title})
        id = db_select(session, (Movie.id,), (Movie.title == title,))
        session.commit()
    return id[0][0]


def add_or_get_user_id(session, id_) -> str:
    id = db_select(session, (User.id,), (User.id == id_,))
    if not id:
        db_insert(session, User, {"id": id_, "name": "user"})
        id = db_select(session, (User.id,), (User.id == id_,))
        session.commit()
    return str(id[0][0])


list_input = [
    (
        {
            "user": "c3a49d5e-d039-4839-85a0-26f261962edb",
            "movie": "Harry Potter",
            "mark": "AWESOME",
        },
        201,
    ),
    (
        {
            "user": "c4a49d5e-d039-4839-85a0-26f261962edb",
            "movie": "Harry Potter",
            "mark": "AWESOME",
        },
        201,
    ),
    (
        {
            "user": "c4a49d5e-d039-4839-85a0-26f261962edb",
            "movie": "Harry Potter",
            "mark": "AWESOME",
        },
        409,
    ),
]

# @pytest.mark.my
@pytest.mark.parametrize(
    "input_data, code",
    list_input,
)
def test_add_mark1(db, client, input_data, code):
    input_data["movie"] = add_or_get_movie_id(db, input_data["movie"])
    input_data["user"] = add_or_get_user_id(db, input_data["user"])

    # print(str(input_data["movie"]), str(input_data["user"]), "-------")
    url = "/api/marks/add-mark"
    response = client.post(url, json=input_data)
    assert response.status_code == code
    # Repeat
    response = client.post(url, json=input_data)
    assert response.status_code == 409
