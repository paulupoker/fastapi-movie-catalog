from typing import Annotated
from fastapi import (
    Depends,
    APIRouter,
    status,
)

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
    "/{slug}/",
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
        **movie.model_dump(),
    )
