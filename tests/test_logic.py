import logging
from uuid import uuid4
import pytest

from sqlalchemy.exc import DBAPIError

from service.db.crud import db_insert, db_select, db_update
from service.db.models import Marks, Movie, User
from service.schemas.marks import MarkSchema
from service.endpoints.utils import (
    AlreadyAddedError,
    NoMarkError,
    NoMovieError,
    NoUserError,
)
from service.utils.logic import add_mark, add_movie, change_mark


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestAddMovieFunc:
    @property
    def title(self):
        return "Title-TestAddMovieFunc"

    async def test_add_new(self, db):
        await add_movie(db, self.title)
        await db.commit()
        titles = await db_select(db, (Movie.title,), (Movie.title == self.title,))
        assert len(titles) == 1
        title = titles[0][0]
        assert title == self.title

    async def test_add_already_existed(self, db):
        with pytest.raises(AlreadyAddedError):
            await add_movie(db, self.title)
            await db.commit()


class TestAddMarkFunc:
    @property
    def input(self):
        return {
            "user_exists": "user_exists",
            "user_not_exists": "user_not_exists",
            "movie_exists": "movie_exists",
            "movie_not_exists": "movie_not_exists",
            "correct_mark": "GOOD",
            "incorrect_mark": "GOOOOOOD",
        }

    # @pytest.mark.my
    async def test_add_new(self, db):
        await db_insert(db, User, {"name": self.input["user_exists"]})
        await db_insert(db, Movie, {"title": self.input["movie_exists"]})
        await db.commit()
        user_id = (
            await db_select(db, (User.id,), (User.name == self.input["user_exists"],))
        )[0][0]
        movie_id = (
            await db_select(
                db, (Movie.id,), (Movie.title == self.input["movie_exists"],)
            )
        )[0][0]

        input_mark = {
            "user": user_id,
            "movie": movie_id,
            "mark": self.input["correct_mark"],
        }
        await add_mark(db, input_mark)

    async def test_add_no_movie(self, db):
        user_id = (
            await db_select(db, (User.id,), (User.name == self.input["user_exists"],))
        )[0][0]
        input_mark = {
            "user": user_id,
            "movie": 1000,
            "mark": self.input["correct_mark"],
        }
        with pytest.raises(NoMovieError):
            await add_mark(db, input_mark)
            await db.commit()

    async def test_add_no_user(self, db):
        input_mark = {
            "user": uuid4(),
            "movie": self.input["movie_exists"],
            "mark": self.input["correct_mark"],
        }
        with pytest.raises(NoUserError):
            await add_mark(db, input_mark)
            await db.commit()

    async def test_add_already_added(self, db):
        try:
            await db_insert(db, User, {"name": self.input["user_exists"]})
            await db.commit()
        except Exception:
            await db.rollback()
        finally:
            user_id = (
                await db_select(
                    db, (User.id,), (User.name == self.input["user_exists"],)
                )
            )[0][0]

        try:
            await db_insert(db, Movie, {"title": self.input["movie_exists"]})
            await db.commit()
        except Exception:
            await db.rollback()
        finally:
            movie_id = (
                await db_select(
                    db, (Movie.id,), (Movie.title == self.input["movie_exists"],)
                )
            )[0][0]

        try:
            await db_insert(
                db,
                Marks,
                {
                    "mark": self.input["correct_mark"],
                    "movie": movie_id,
                    "user": user_id,
                },
            )
            await db.commit()
        except Exception:
            await db.rollback()

        input_mark = {
            "user": user_id,
            "movie": movie_id,
            "mark": self.input["correct_mark"],
        }
        with pytest.raises(AlreadyAddedError):
            await add_mark(db, input_mark)
            await db.commit()

    # @pytest.mark.my
    async def test_add_incorrect(self, db):
        try:
            await db_insert(db, User, {"name": "test_add_incorrect"})
            await db.commit()
        except Exception:
            await db.rollback()
        finally:
            user_id = (
                await db_select(db, (User.id,), (User.name == "test_add_incorrect",))
            )[0][0]

        try:
            await db_insert(db, Movie, {"title": self.input["movie_exists"]})
            await db.commit()
        except Exception:
            await db.rollback()
        finally:
            movie_id = (
                await db_select(
                    db, (Movie.id,), (Movie.title == self.input["movie_exists"],)
                )
            )[0][0]

        input_mark = {
            "user": user_id,
            "movie": movie_id,
            "mark": self.input["incorrect_mark"],
        }
        with pytest.raises(DBAPIError):
            await add_mark(db, input_mark)
            await db.commit()


class TestChangeMarkFunc:
    @property
    def input(self):
        return {
            "user_exists": "user_exists",
            "user_not_exists": "user_not_exists",
            "movie_exists": "movie_exists",
            "movie_not_exists": "movie_not_exists",
            "correct_mark": "GOOD",
            "incorrect_mark": "GOOOOOOD",
        }

    # @pytest.mark.my
    async def test_change_successful(self, db):
        try:
            await db_insert(db, User, {"name": self.input["user_exists"]})
            await db.commit()
        except Exception:
            await db.rollback()
        finally:
            user_id = (
                await db_select(
                    db, (User.id,), (User.name == self.input["user_exists"],)
                )
            )[0][0]

        try:
            await db_insert(db, Movie, {"title": self.input["movie_exists"]})
            await db.commit()
        except Exception:
            await db.rollback()
        finally:
            movie_id = (
                await db_select(
                    db, (Movie.id,), (Movie.title == self.input["movie_exists"],)
                )
            )[0][0]

        try:
            await db_insert(
                db,
                Marks,
                {
                    "mark": self.input["correct_mark"],
                    "movie": movie_id,
                    "user": user_id,
                },
            )
            await db.commit()
        except Exception:
            await db.rollback()

        input_mark = {
            "user": user_id,
            "movie": movie_id,
            "mark": self.input["correct_mark"],
        }
        await change_mark(db, input_mark)
        await db.commit()

    @pytest.mark.my
    async def test_no_mark_to_change(self, db):
        try:
            await db_insert(db, User, {"name": "test_no_mark_to_change"})
            await db.commit()
        except Exception:
            await db.rollback()
        finally:
            user_id = (
                await db_select(
                    db, (User.id,), (User.name == "test_no_mark_to_change",)
                )
            )[0][0]

        try:
            await db_insert(db, Movie, {"title": self.input["movie_exists"]})
            await db.commit()
        except Exception:
            await db.rollback()
        finally:
            movie_id = (
                await db_select(
                    db, (Movie.id,), (Movie.title == self.input["movie_exists"],)
                )
            )[0][0]
            await db.commit()

        input_mark = {
            "user": user_id,
            "movie": movie_id,
            "mark": self.input["correct_mark"],
        }
        with pytest.raises(NoMarkError):
            await change_mark(db, input_mark)
