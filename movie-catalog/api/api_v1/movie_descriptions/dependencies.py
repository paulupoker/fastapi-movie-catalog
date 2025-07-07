from fastapi import (
    HTTPException,
    status,
)

from .crud import MOVIES
from schemas.movies import Movie


def prefetch_movie(
    movie_slug: str,
) -> Movie:

    movie: Movie | None = next(
        (movie for movie in MOVIES if movie.slug == movie_slug),
        None,
    )
    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug {movie_slug!r} not found",
    )
