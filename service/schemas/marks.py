import uuid
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class MarkSchema(str, Enum):
    AWESOME = "AWESOME"
    GREAT = "GREAT"
    GOOD = "GOOD"
    NOT_BAD = "NOT_BAD"
    BAD = "BAD"


class MarkInputSchema(BaseModel):
    user: uuid.UUID = Field(example=uuid.uuid4(), description="user_id")
    movie: int = Field(example=1)
    mark: MarkSchema = Field(example="AWESOME", description="mark of the movie")
