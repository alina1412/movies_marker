from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from service.db.models import Marks, Movie, User
from service.schemas.marks import MarkSchema


async def db_insert(session: AsyncSession, model, dict_data):
    query = insert(model).values(**dict_data)
    await session.execute(query)
    # await session.commit()


async def db_select(session: AsyncSession, what, condition):
    query = select(*what).where(*condition)
    results = (await session.execute(query)).all()
    return list(results)


async def db_update(session: AsyncSession, what, condition, new_data):
    try:
        stmt = update(*what).where(*condition).values(**new_data)
        await session.execute(stmt)
        # await session.commit()
    except Exception as e:
        print(e)
        await session.rollback()
        return False
