from typing import Annotated
from fastapi import (
    Depends,
    APIRouter,
    status,
)

from .dependencies import (
    prefetch_movie,
)
from .crud import storage
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
def read_movie_list() -> list[Movie]:
    return storage.get()


@router.get(
    "/{slug}/",
    response_model=Movie,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": f"Movie with slug 'slug' not found",
                    },
                },
            },
        },
    },
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
    return storage.create(movie)


@router.delete(
    "/{slug}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": f"Movie with slug 'slug' not found",
                    },
                },
            },
        },
    },
)
def delete_movie(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie),
    ],
) -> None:
    storage.delete(movie=movie)
