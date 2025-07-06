from pydantic import (
    BaseModel,
    AnyHttpUrl,
    Field,
)
from typing import Annotated


class MovieDescriptionBase(BaseModel):
    slug: str
    title: str
    description: str
    genre: str
    year: int
    director: str
    rating: float
    url: AnyHttpUrl


class MovieDescription(MovieDescriptionBase):
    """
    Movie description model.
    """


class MovieDescriptionCreate(BaseModel):
    """
    Model for creation movie description.
    """

    slug: str = Field(max_length=30)
    title: str = Field(max_length=100)
    description: str = Field(max_length=1000)
    genre: str = Field(max_length=100)
    year: int = Field(ge=1900, le=3000)
    director: str = Field(max_length=100)
    rating: float = Field(ge=1, le=10)
    url: Annotated[str, AnyHttpUrl]
