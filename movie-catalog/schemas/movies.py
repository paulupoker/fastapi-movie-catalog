from pydantic import (
    BaseModel,
    AnyHttpUrl,
    Field,
)
from typing import Annotated

SlugString = Annotated[str, Field(min_length=3, max_length=30)]
TitleString = Annotated[str, Field(min_length=2, max_length=100)]
DescriptionString = Annotated[str, Field(min_length=2, max_length=1000)]
GenreString = Annotated[str, Field(min_length=2, max_length=100)]
YearInt = Annotated[int, Field(ge=1900, le=3000)]
DirectorString = Annotated[str, Field(min_length=2, max_length=100)]
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
    notes: str | None = None


class MovieRead(MovieBase):
    """
    Model for reading movie data.
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


class MoviePartialUpdate(MovieBase):
    """
    Model for partial movie update.
    """

    title: TitleString | None = None
    description: DescriptionString | None = None
    genre: GenreString | None = None
    year: YearInt | None = None
    director: DirectorString | None = None
    rating: RatingFloat | None = None
    url: AnyHttpUrl | None = None
