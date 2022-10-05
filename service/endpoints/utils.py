from service.schemas.marks import MarkInputSchema


class NoUserError(Exception):
    detail: str = "no such user"


class AlreadyAddedError(Exception):
    detail: str = "mark had been already added"
