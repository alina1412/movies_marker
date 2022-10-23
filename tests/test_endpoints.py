import logging
import uuid
from uuid import UUID

import pytest

from service.db.crud import db_insert, db_select, db_update
from service.db.models import Marks, Movie, User
from service.schemas.marks import MarkSchema
from tests.utils import (
    add_or_get_fake_prev_mark,
    add_or_get_movie_id,
    add_or_get_user_id,
)


# @pytest.mark.my
async def test_add_movie(db, client):
    url = "/api/v1/add-movie"
    lst = [("Title1", 201), ("Title2", 201), ("", 422)]
    for title, code in lst:
        id = await db_select(db, (Movie.id,), (Movie.title == title,))
        assert not id

        response = client.put(url + f"?title={title}")
        assert response.status_code == code

        id = await db_select(db, (Movie.id,), (Movie.title == title,))
        if code == 201:
            assert id
        else:
            assert not id


def validate_user(input_data):
    try:
        uuid_obj = UUID(input_data.get("user", "None"), version=4)
    except ValueError:
        return False
    return True


def validate_movie(input_data):
    if not input_data.get("movie", None):
        return False
    return True


def validate_mark(input_data):
    mark = input_data.get("mark", None)
    if mark not in (
        MarkSchema.AWESOME,
        MarkSchema.GREAT,
        MarkSchema.GOOD,
        MarkSchema.NOT_BAD,
        MarkSchema.BAD,
    ):
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


# @pytest.mark.my
@pytest.mark.parametrize(
    "input_data, code",
    list_input,
)
async def test_add_mark(db, client, input_data, code):
    if validate_user(input_data) and validate_movie(input_data):
        input_data["movie"] = await add_or_get_movie_id(
            db, input_data.get("movie", None)
        )
        input_data["user"] = await add_or_get_user_id(db, input_data.get("user", None))

    url = "/api/v1/add-mark"
    response = client.post(url, json=input_data)
    assert response.status_code == code


list_input = [
    (
        {
            "user": "c3a49d5e-d039-4839-85a0-26f261962edb",
            "movie": "Harry Potter",
            "mark": "BAD",
        },
        200,
    ),
    (
        {
            "user": "c4a49d5e-d039-4839-85a0-26f261962edb",
            "movie": "Harry Potter",
            "mark": "BAD",
        },
        200,
    ),
]
# @pytest.mark.my
@pytest.mark.parametrize(
    "input_data, code",
    list_input,
)
async def test_change_existing_mark(db, client, input_data, code):
    if validate_user(input_data) and validate_movie(input_data):
        input_data["movie"] = await add_or_get_movie_id(
            db, input_data.get("movie", None)
        )
        input_data["user"] = await add_or_get_user_id(db, input_data.get("user", None))
        prev_id = await add_or_get_fake_prev_mark(db, input_data)

    url = "/api/v1/change-mark"
    response = client.post(url, json=input_data)
    assert response.status_code == code


# @pytest.mark.my
@pytest.mark.parametrize(
    "input_data",
    [
        {
            "user": "c4a49d5e-d039-4839-85a0-26f261962edb",
            "movie": uuid.uuid4().hex,
            "mark": "BAD",
        },
    ],
)
async def test_change_unexisting_mark(db, client, input_data):
    if validate_user(input_data) and validate_movie(input_data):
        input_data["movie"] = await add_or_get_movie_id(
            db, input_data.get("movie", None)
        )
        input_data["user"] = await add_or_get_user_id(db, input_data.get("user", None))
    url = "/api/v1/change-mark"
    response = client.post(url, json=input_data)
    assert response.status_code == 421


# @pytest.mark.my
@pytest.mark.parametrize(
    "input_data",
    [
        {
            "user": "c4a49d5e-d039-4839-85a0-26f261972edb",  # no user
            "movie": uuid.uuid4().hex,
            "mark": "BAD",
        },
    ],
)
async def test_change_mark_errors(db, client, input_data):
    if validate_user(input_data) and validate_movie(input_data):
        input_data["movie"] = await add_or_get_movie_id(
            db, input_data.get("movie", None)
        )

    url = "/api/v1/change-mark"
    response = client.post(url, json=input_data)
    assert response.status_code == 404
