from service.db.crud import db_insert, db_select, db_update
from service.db.models import Marks, Movie, User


async def add_or_get_movie_id(session, title) -> int:
    id = await db_select(session, (Movie.id,), (Movie.title == title,))
    if not id:
        await db_insert(session, Movie, {"title": title})
        id = await db_select(session, (Movie.id,), (Movie.title == title,))
        await session.commit()
    return id[0][0]


async def add_or_get_user_id(session, id_) -> str:
    id = await db_select(session, (User.id,), (User.id == id_,))
    if not id:
        await db_insert(session, User, {"id": id_, "name": "user"})
        id = await db_select(session, (User.id,), (User.id == id_,))
        await session.commit()
    return str(id[0][0])


async def select_mark_id(session, input_data) -> int:
    return await db_select(
        session,
        (Marks.id,),
        (
            Marks.user == input_data["user"],
            Marks.movie == input_data["movie"],
        ),
    )


async def add_or_get_fake_prev_mark(session, input_data) -> int:
    id = await select_mark_id(session, input_data)
    if not id:
        await db_insert(
            session,
            Marks,
            {
                "user": input_data["user"],
                "movie": input_data["movie"],
                "mark": "GOOD",
            },
        )
        id = await select_mark_id(session, input_data)
        await session.commit()
    return id[0][0]
