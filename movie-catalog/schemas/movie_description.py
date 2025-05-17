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


class MovieDescription(MovieDescriptionBase):
    """
    Movie description model.
    """

    pass
