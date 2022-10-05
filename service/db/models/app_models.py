import uuid
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from service.db import DeclarativeBase
from service.schemas.marks import MarkSchema


class User(DeclarativeBase):
    __tablename__ = "user"

    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"User(name={self.name})"


class Movie(DeclarativeBase):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, unique=True)

    def __repr__(self):
        return f"title={self.title}"


class Marks(DeclarativeBase):
    __tablename__ = "marks"

    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    user = Column(ForeignKey("user.id"), nullable=False)
    movie = Column(ForeignKey("movie.id"), nullable=False)
    mark = Column(Enum(MarkSchema), nullable=False)

    def __repr__(self):
        return f"TestModel(id={self.id}, name={self.name})"
