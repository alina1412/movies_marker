from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from service.db.crud import db_insert, db_select, db_update
from service.db.models import Marks, Movie, User
from service.endpoints.utils import AlreadyAddedError, NoUserError
from service.schemas.marks import MarkInputSchema


async def add_movie(session: AsyncSession, title: str):
    await db_insert(session, Movie, {"title": title})


async def add_mark(session: AsyncSession, input_mark: dict):
    input_mark["user"] = str(input_mark["user"]).replace("-", "")
    print(input_mark["user"], "add_mark")
    user_id = await get_user_id(session, input_mark["user"])
    if not user_id:
        raise NoUserError
    if await db_select(
        session,
        (Marks.id,),
        (Marks.user == user_id, Marks.movie == input_mark["movie"]),
    ):
        raise AlreadyAddedError
    await db_insert(session, Marks, input_mark)


async def change_mark(session: AsyncSession, input_mark: MarkInputSchema):
    input_mark["user"] = str(input_mark["user"]).replace("-", "")
    user_id = await get_user_id(session, input_mark["user"])
    if not user_id:
        raise NoUserError
    await db_update(
        session,
        (Marks,),
        (Marks.user == input_mark["user"], Marks.movie == input_mark["movie"]),
        {"mark": input_mark["mark"]},
    )


async def get_user_id(session: AsyncSession, id_: UUID4):
    res = await db_select(session, (User.id,), (User.id == id_,))
    if not res:
        return None
    return res[0][0]


async def get_rows(session, what, condition):
    res = await db_select(session, what, condition)
    # res = await db_select(session, (User.id,), (User.name=="user",))
    print(res)
    return res
