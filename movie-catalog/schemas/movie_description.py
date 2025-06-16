from pydantic import (
    BaseModel,
)


class MovieDescriptionBase(BaseModel):
    id: int
    title: str
    description: str
    genre: str
    year: int
    director: str
    rating: float


class MovieDescription(MovieDescriptionBase):
    """
    Movie description model.
    """

    pass
