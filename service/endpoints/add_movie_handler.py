import logging

from fastapi import APIRouter, Depends, Query, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from service.db.connection import get_session
from service.endpoints.utils import AlreadyAddedError
from service.utils.logic import add_movie

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


api_router = APIRouter(
    prefix="/v1",
    tags=["movie"],
)


@api_router.put(
    "/add-movie",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_409_CONFLICT: {"description": "This movie had been added already"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def add_movie_handler(
    _: Request,
    title: str = Query(min_length=1, max_length=255),
    session: AsyncSession = Depends(get_session),
):
    """Add a unique title"""
    if not title:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    try:
        await add_movie(session, title)
        return
    except AlreadyAddedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT) from exc
    except (IntegrityError, Exception) as exc:
        logger.debug(exc)
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
