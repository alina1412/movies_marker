import logging

from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from service.db.connection import get_session
from service.utils.logic import add_movie

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


api_router = APIRouter(
    prefix="/movie",
    tags=["movie"],
)


@api_router.post(
    "/add-movie",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def add_movie_handler(
    _: Request,
    title: str,
    session: AsyncSession = Depends(get_session),
):
    """Add a unique title"""
    try:
        await add_movie(session, title)
        return
    except (IntegrityError, Exception) as exc:
        logger.debug(exc)
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
