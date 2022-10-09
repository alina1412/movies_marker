class NoUserError(Exception):
    detail: str = "no such user"


class AlreadyAddedError(Exception):
    detail: str = "item already exists"


class NoMovieError(Exception):
    detail: str = "no such movie"


class NoMarkError(Exception):
    detail: str = "no such mark"
