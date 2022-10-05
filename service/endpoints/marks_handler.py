import logging

from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from service.db.connection import get_session
from service.endpoints.utils import AlreadyAddedError, NoUserError
from service.schemas.marks import MarkInputSchema
from service.utils.logic import add_mark, change_mark

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


api_router = APIRouter(
    prefix="/marks",
    tags=["marks"],
)


@api_router.post(
    "/add-mark",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
        status.HTTP_409_CONFLICT: {
            "description": "This mark had been added, use 'change' method"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
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
        return
    except NoUserError as exc:
        logger.debug(f"---NoUserError")
        raise HTTPException(status.HTTP_404_NOT_FOUND) from exc
    except AlreadyAddedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT) from exc
    except IntegrityError:
        logger.debug(f"---IntegrityError")
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.debug(e)
        raise HTTPException(status.HTTP_400_BAD_REQUEST)


@api_router.post(
    "/change-mark",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
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
        return
    except NoUserError:
        logger.debug("---NoUserError")
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    except IntegrityError:
        logger.debug("---IntegrityError")
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.debug(e)
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
