from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from service.config.default import logger
from service.db.connection import get_session
from service.endpoints.utils import (
    AlreadyAddedError,
    NoMarkError,
    NoMovieError,
    NoUserError,
)
from service.schemas.marks import MarkInputSchema
from service.utils.logic import add_mark, change_mark

api_router = APIRouter(
    prefix="/v1",
    tags=["marks"],
)


@api_router.post(
    "/add-mark",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_404_NOT_FOUND: {"description": "User or movie not found"},
        status.HTTP_409_CONFLICT: {
            "description": """Mark to this movie exists already,
              use 'change' method"""
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Not correct request"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error"
        },
    },
)
async def add_mark_handler(
    _: Request,
    input_mark: MarkInputSchema,
    session: AsyncSession = Depends(get_session),
):
    """Add a mark for a movie"""
    try:
        await add_mark(session, input_mark.dict())
    except (NoUserError, NoMovieError) as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=exc.detail
        ) from exc
    except AlreadyAddedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT) from exc
    except (IntegrityError, Exception) as exc:
        logger.error(exc_info=exc)
        raise HTTPException(status.HTTP_400_BAD_REQUEST)


@api_router.post(
    "/change-mark",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_404_NOT_FOUND: {"description": "User or movie not found"},
        421: {"description": NoMarkError.detail},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Not correct request"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error"
        },
    },
)
async def change_mark_handler(
    _: Request,
    input_mark: MarkInputSchema,
    session: AsyncSession = Depends(get_session),
):
    """Change user's existing mark of a movie"""
    try:
        await change_mark(session, input_mark.dict())
    except NoMarkError as exc:
        raise HTTPException(status_code=421, detail=NoMarkError.detail) from exc
    except (NoUserError, NoMovieError) as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=exc.detail
        ) from exc
    except (IntegrityError, Exception) as exc:
        logger.error(exc_info=exc)
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
