import pytest

from service.db.crud import db_insert, db_select, db_update
from service.db.models import Marks, Movie, User
from service.schemas.marks import MarkSchema


async def add_example_user(session, user_data):
    await db_insert(session, User, user_data)
    res = await db_select(session, (User.id,), (User.name == user_data["name"],))
    assert res != []
    user_id = res[0][0]
    return user_id


async def add_example_movie(session, movie_data):
    await db_insert(session, Movie, movie_data)
    res = await db_select(session, (Movie.id,), (Movie.title == movie_data["title"],))
    assert res != []
    movie_id = res[0][0]
    return movie_id


async def add_example_mark(session, mark_data, user_id, movie_id):
    await db_insert(
        session,
        Marks,
        dict(mark=mark_data["mark"], user=user_id, movie=movie_id),
    )
    res = await db_select(session, (Marks.id,), (Marks.movie == movie_id,))
    assert res != []


# @pytest.mark.my
async def test_db(db):
    """fill db and check"""
    user_data = {"name": "3"}
    movie_data = {"title": "HP"}
    mark_data = {"mark": MarkSchema.AWESOME}

    try:
        user_id = await add_example_user(db, user_data)
        movie_id = await add_example_movie(db, movie_data)
        await add_example_mark(db, mark_data, user_id, movie_id)
    except Exception as exc:
        await db.rollback()
        raise exc

    await db_update(db, (User,), (User.name == user_data["name"],), {"name": "user2"})
    await db.commit()

    res = await db_select(db, (User.name,), (User.name == "user2",))
    assert res != []
