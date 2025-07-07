from typing import Annotated
from fastapi import (
    Depends,
    APIRouter,
    status,
)

from .dependencies import (
    prefetch_movie,
)
from .crud import MOVIES
from schemas.movies import (
    Movie,
    MovieCreate,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[Movie],
)
def read_movie_list():
    return MOVIES


@router.get(
    "/{slug}/",
    response_model=Movie,
)
def read_movie(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie),
    ],
) -> Movie:

    return movie


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie: MovieCreate,
) -> Movie:

    return Movie(
        **movie.model_dump(),
    )
