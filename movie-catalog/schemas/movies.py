from pydantic import (
    BaseModel,
    AnyHttpUrl,
    Field,
)
from typing import Annotated

SlugString = Annotated[str, Field(max_length=30)]
TitleString = Annotated[str, Field(max_length=100)]
DescriptionString = Annotated[str, Field(max_length=1000)]
GenreString = Annotated[str, Field(max_length=100)]
YearInt = Annotated[int, Field(ge=1900, le=3000)]
DirectorString = Annotated[str, Field(max_length=100)]
RatingFloat = Annotated[float, Field(ge=1, le=10)]


class MovieBase(BaseModel):
    title: str
    description: str
    genre: str
    year: int
    director: str
    rating: float
    url: AnyHttpUrl


class Movie(MovieBase):
    """
    Movie model.
    """

    slug: str


class MovieCreate(MovieBase):
    """
    Model for creating a movie.
    """

    slug: SlugString
    title: TitleString
    description: DescriptionString
    genre: GenreString
    year: YearInt
    director: DirectorString
    rating: RatingFloat


class MovieUpdate(MovieBase):
    """
    Model for updating a movie.
    """

    title: TitleString
    description: DescriptionString
    genre: GenreString
    year: YearInt
    director: DirectorString
    rating: RatingFloat
