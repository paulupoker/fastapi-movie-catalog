from pydantic import (
    BaseModel,
    AnyHttpUrl,
    Field,
)


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

    slug: str = Field(max_length=30)
    title: str = Field(max_length=100)
    description: str = Field(max_length=1000)
    genre: str = Field(max_length=100)
    year: int = Field(ge=1900, le=3000)
    director: str = Field(max_length=100)
    rating: float = Field(ge=1, le=10)


class MovieUpdate(MovieBase):
    """
    Model for updating a movie.
    """

    title: str = Field(max_length=100)
    description: str = Field(max_length=1000)
    genre: str = Field(max_length=100)
    year: int = Field(ge=1900, le=3000)
    director: str = Field(max_length=100)
    rating: float = Field(ge=1, le=10)
