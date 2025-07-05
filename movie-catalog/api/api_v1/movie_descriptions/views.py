from typing import Annotated
from random import randint
from fastapi import (
    Depends,
    APIRouter,
    status,
    Form,
)
from annotated_types import MaxLen
from pydantic import AnyHttpUrl

from .dependencies import (
    prefetch_movie_description,
)
from .crud import MOVIES
from schemas.movie_description import MovieDescription

router = APIRouter(
    prefix="/movies",
    tags=["Movie Descriptions"],
)


@router.get(
    "/",
    response_model=list[MovieDescription],
)
def read_movie_list():
    return MOVIES


@router.get(
    "/{id}/",
    response_model=MovieDescription,
)
def read_movie(
    movie: Annotated[
        MovieDescription,
        Depends(prefetch_movie_description),
    ],
) -> MovieDescription:

    return movie


@router.post(
    "/",
    response_model=MovieDescription,
    status_code=status.HTTP_201_CREATED,
)
def add_movie(
    title: Annotated[str, MaxLen(100), Form()],
    description: Annotated[str, MaxLen(1000), Form()],
    genre: Annotated[str, MaxLen(100), Form()],
    year: Annotated[int, Form()],
    director: Annotated[str, MaxLen(100), Form()],
    rating: Annotated[float, Form()],
    url: Annotated[AnyHttpUrl, Form()],
) -> MovieDescription:
    return MovieDescription(
        id=randint(1, 1000),
        title=title,
        description=description,
        genre=genre,
        year=year,
        director=director,
        rating=rating,
        url=url,
    )
