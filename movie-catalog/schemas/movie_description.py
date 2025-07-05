from pydantic import (
    BaseModel,
    AnyHttpUrl,
)


class MovieDescriptionBase(BaseModel):
    id: int
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

    pass
