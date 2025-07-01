from fastapi import HTTPException
from starlette import status

from .crud import MOVIES
from schemas.movie_description import MovieDescription


def prefetch_movie_description(
    movie_id: int,
) -> MovieDescription:

    movie: MovieDescription | None = next(
        (movie for movie in MOVIES if movie.id == movie_id),
        None,
    )
    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with id {movie_id} not found",
    )
