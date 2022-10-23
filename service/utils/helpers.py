from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from service.db.crud import db_select
from service.db.models import Marks, Movie, User


async def get_user_by_id(session: AsyncSession, user_id: UUID4) -> str:
    id_ = str(user_id).replace("-", "")
    res = await db_select(session, (User.id,), (User.id == id_,))
    if not res:
        return None
    user_id = res[0][0]
    return user_id


async def is_movie_exists(session: AsyncSession, condition) -> bool:
    if await db_select(session, (Movie.id,), (condition)):
        return True
    return False


async def is_mark_exists(session: AsyncSession, user_id: str, movie_id: int) -> bool:
    if await db_select(
        session,
        (Marks.id,),
        (Marks.user == user_id, Marks.movie == movie_id),
    ):
        return True
    return False
