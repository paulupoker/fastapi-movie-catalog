from typing import Annotated
from fastapi import (
    Depends,
    APIRouter,
    status,
)
from random import randint

from .dependencies import (
    prefetch_movie_description,
)
from .crud import MOVIES
from schemas.movie_description import (
    MovieDescription,
    MovieDescriptionCreate,
)

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
def create_movie(
    movie: MovieDescriptionCreate,
) -> MovieDescription:

    return MovieDescription(
        id=randint(1, 1000),
        **movie.model_dump(),
    )
