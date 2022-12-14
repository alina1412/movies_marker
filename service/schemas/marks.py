import uuid
from enum import Enum

from pydantic import UUID4, BaseModel, Field


class MarkSchema(str, Enum):
    AWESOME = "AWESOME"
    GREAT = "GREAT"
    GOOD = "GOOD"
    NOT_BAD = "NOT_BAD"
    BAD = "BAD"


class MarkInputSchema(BaseModel):
    user: UUID4 = Field(example=uuid.uuid4(), description="user_id")
    movie: int = Field(example=1)
    mark: MarkSchema = Field(example="AWESOME", description="mark of the movie")
