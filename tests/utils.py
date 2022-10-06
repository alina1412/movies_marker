from sqlalchemy import insert, select, update


def db_insert(session, model, dict_data):
    query = insert(model).values(**dict_data)
    session.execute(query)


def db_select(session, what, condition):
    query = select(*what).where(*condition)
    results = (session.execute(query)).all()
    return list(results)


def db_update(session, what, condition, new_data):
    q = update(*what).where(*condition).values(**new_data)
    session.execute(q)
