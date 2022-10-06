import pytest

from service.db.models import Marks, Movie, User
from service.schemas.marks import MarkSchema
from tests.utils import db_insert, db_select, db_update


def prepare_fill(db, user_data, movie_data, mark_data):
    with db as session:
        with session.begin():
            # User
            db_insert(session, User, user_data)
            res = db_select(
                session, (User.id,), (User.name == user_data["name"],)
            )
            assert res != []
            user_id = res[0][0]
            print(user_id, "------")

            # Movie
            db_insert(session, Movie, movie_data)
            res = db_select(
                session, (Movie.id,), (Movie.title == movie_data["title"],)
            )
            assert res != []
            movie_id = res[0][0]
            print(movie_id, "------")

            # Marks
            db_insert(
                session,
                Marks,
                dict(mark=mark_data["mark"], user=user_id, movie=movie_id),
            )
            res = db_select(session, (Marks.id,), (Marks.movie == movie_id,))
            assert res != []

            session.commit()
            return True


# @pytest.mark.my
def test_db(db):
    """fill db and check"""
    user_data = {"name": "3"}
    movie_data = {"title": "HP"}
    mark_data = {"mark": MarkSchema.AWESOME}

    try:
        prepare_fill(db, user_data, movie_data, mark_data)
    except Exception as e:
        db.rollback()
        raise e

    db_update(db, (User,), (User.name == user_data["name"],), {"name": "user2"})
    db.commit()

    res = db_select(db, (User.name,), (User.name == "user2",))
    assert res != []
