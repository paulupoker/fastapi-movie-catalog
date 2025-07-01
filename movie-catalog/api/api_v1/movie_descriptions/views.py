from typing import Annotated

from fastapi import Depends, APIRouter

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
