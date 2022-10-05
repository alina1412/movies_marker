from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from service.db.connection import get_session
from service.endpoints.utils import AlreadyAddedError, NoUserError
from service.schemas.marks import MarkInputSchema
from service.utils.logic import add_mark, change_mark

api_router = APIRouter(
    prefix="/marks",
    tags=["marks"],
)


@api_router.post(
    "/add-mark",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
        status.HTTP_409_CONFLICT: {
            "description": "mark had been added, use change method"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def add_mark_handler(
    _: Request,
    input_mark: MarkInputSchema,
    session: AsyncSession = Depends(get_session),
):
    """ """
    try:
        await add_mark(session, input_mark.dict())
        return
    except NoUserError:
        print("---NoUserError")
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    except AlreadyAddedError:
        raise HTTPException(status.HTTP_409_CONFLICT)
    except IntegrityError:
        print("---IntegrityError")
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
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
    """ """
    try:
        await change_mark(session, input_mark.dict())
        return
    except NoUserError:
        print("---NoUserError")
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    except IntegrityError:
        print("---IntegrityError")
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
