import json
import logging
from uuid import UUID

import pytest

from service.db.models import Marks, Movie, User
from tests.utils import db_insert, db_select, db_update


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


@pytest.mark.my
def test_add_movie(client, db):
    url = "/api/v1/add-movie"
    lst = ["Title1", "Title2"]
    for title in lst:
        id = db_select(db, (Movie.id,), (Movie.title == title,))
        assert not id

        response = client.put(url + f"?title={title}")
        assert response.status_code == 201

        id = db_select(db, (Movie.id,), (Movie.title == title,))
        assert id


def validate_input_data(input_data):
    try:
        uuid_obj = UUID(input_data.get("user", "None"), version=4)
    except ValueError:
        return False

    if not input_data.get("movie", None):
        return False
    return True


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
    (
        {
            "user": "c4a49d5e-d039-4839-85a0-26f261962edb",
            "movie": "Harry Potter",
            "mark": "A",
        },
        422,
    ),
    (
        {
            "user": "c4a49d5e-d039-",
            "movie": "Harry Potter",
            "mark": "AWESOME",
        },
        422,
    ),
    (
        {
            "user": "c4a49d5e-d039-4839-85a0-26f261962edb",
            "movie": "",
            "mark": "AWESOME",
        },
        422,
    ),
    (
        {
            "mark": "AWESOME",
        },
        422,
    ),
    (
        {
            "user": "c4a49d5e-d039-4839-85a0-26f261962edb",
            "movie": "HP",
        },
        422,
    ),
]


@pytest.mark.my
@pytest.mark.parametrize(
    "input_data, code",
    list_input,
)
def test_add_mark1(db, client, input_data, code):
    if validate_input_data(input_data):
        input_data["movie"] = add_or_get_movie_id(db, input_data.get("movie", None))
        input_data["user"] = add_or_get_user_id(db, input_data.get("user", None))

    url = "/api/v1/add-mark"
    response = client.post(url, json=input_data)
    assert response.status_code == code
