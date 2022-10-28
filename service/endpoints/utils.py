class NoUserError(Exception):
    detail: str = "no such user"


class AlreadyAddedError(Exception):
    detail: str = "Item already exists"


class NoMovieError(Exception):
    detail: str = "No such movie"


class NoMarkError(Exception):
    detail: str = "No such mark"
