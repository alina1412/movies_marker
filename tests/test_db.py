import pytest
from sqlalchemy import insert, select, update

from service.db.models import Marks, Movie, User
from service.schemas.marks import MarkSchema

pytestmark = pytest.mark.asyncio


async def db_insert(session, model, dict_data):
    query = insert(model).values(**dict_data)
    session.execute(query)


async def db_select(session, what, condition):
    query = select(*what).where(*condition)
    results = (session.execute(query)).all()
    return list(results)


async def db_update(session, what, condition, new_data):
    q = update(*what).where(*condition).values(**new_data)
    session.execute(q)


async def prepare_fill(db, user_data, movie_data, mark_data):
    with db as session:
        with session.begin():
            # User
            await db_insert(session, User, user_data)
            res = await db_select(session, (User.id,), (User.name == user_data["name"],))
            assert res != []
            user_id = res[0][0]
            print(user_id, "------")

            # Movie
            await db_insert(session, Movie, movie_data)
            res = await db_select(session, (Movie.id,), (Movie.title == movie_data["title"],))
            assert res != []
            movie_id = res[0][0]
            print(movie_id, "------")

            # Marks
            await db_insert(session, Marks, dict(mark=mark_data["mark"], user=user_id, movie=movie_id))
            res = await db_select(session, (Marks.id,), (Marks.movie == movie_id,))
            assert res != []

            session.commit()
            return True


async def test_sample2(db):
    """fill db and check"""
    user_data = {"name": "3"}
    movie_data = {"title": "HP"}
    mark_data = {"mark": MarkSchema.AWESOME}

    try:
        await prepare_fill(db, user_data, movie_data, mark_data)
    except Exception as e:
        db.rollback()
        raise e

    await db_update(db, (User,), (User.name == user_data["name"],), {"name": "user2"})
    db.commit()

    res = await db_select(db, (User.name,), (User.name == "user2",))
    assert res != []
