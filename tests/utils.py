from sqlalchemy import insert, select, update

from service.db.models import Marks, Movie, User


def db_insert(session, model, dict_data):
    query = insert(model).values(**dict_data)
    session.execute(query)


def db_select(session, what, condition):
    query = select(*what).where(*condition)
    results = (session.execute(query)).all()
    return list(results)


def db_update(session, what, condition, new_data):
    query = update(*what).where(*condition).values(**new_data)
    session.execute(query)


def add_or_get_movie_id(session, title) -> int:
    id = db_select(session, (Movie.id,), (Movie.title == title,))
    if not id:
        db_insert(session, Movie, {"title": title})
        id = db_select(session, (Movie.id,), (Movie.title == title,))
        session.commit()
    return id[0][0]


def add_or_get_user_id(session, id_) -> str:
    id = db_select(session, (User.id,), (User.id == id_,))
    if not id:
        db_insert(session, User, {"id": id_, "name": "user"})
        id = db_select(session, (User.id,), (User.id == id_,))
        session.commit()
    return str(id[0][0])


def select_mark_id(session, input_data) -> int:
    return db_select(
        session,
        (Marks.id,),
        (
            Marks.user == input_data["user"],
            Marks.movie == input_data["movie"],
        ),
    )


def add_or_get_fake_prev_mark(session, input_data) -> int:
    id = select_mark_id(session, input_data) 
    if not id:
        db_insert(
            session,
            Marks,
            {
                "user": input_data["user"],
                "movie": input_data["movie"],
                "mark": "GOOD",
            },
        )
        id = select_mark_id(session, input_data) 
        session.commit()
    return id[0][0]
