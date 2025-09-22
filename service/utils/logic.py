from sqlalchemy.ext.asyncio import AsyncSession

from service.db.crud import db_insert, db_update
from service.db.models import Marks, Movie
from service.endpoints.utils import (
    AlreadyAddedError,
    NoMarkError,
    NoMovieError,
    NoUserError,
)
from service.utils.helpers import (
    get_user_by_id,
    is_mark_exists,
    is_movie_exists,
)


async def add_movie(session: AsyncSession, title: str) -> None:
    if await is_movie_exists(session, (Movie.title == title,)):
        raise AlreadyAddedError
    await db_insert(session, Movie, {"title": title})


async def add_mark(session: AsyncSession, input_mark: dict) -> None:
    input_mark["user"] = user_id = await get_user_by_id(
        session, input_mark["user"]
    )
    if not user_id:
        raise NoUserError
    if not await is_movie_exists(session, (Movie.id == input_mark["movie"],)):
        raise NoMovieError
    if await is_mark_exists(session, user_id, input_mark["movie"]):
        raise AlreadyAddedError
    await db_insert(session, Marks, input_mark)


async def change_mark(session: AsyncSession, input_mark: dict) -> None:
    user_id = await get_user_by_id(session, input_mark["user"])
    if not user_id:
        raise NoUserError
    if not await is_movie_exists(session, (Movie.id == input_mark["movie"],)):
        raise NoMovieError
    if not await is_mark_exists(session, user_id, input_mark["movie"]):
        raise NoMarkError
    await db_update(
        session,
        (Marks,),
        (Marks.user == user_id, Marks.movie == input_mark["movie"]),
        {"mark": input_mark["mark"]},
    )
