from fastapi import HTTPException
from starlette import status

from .crud import MOVIES
from schemas.movie_description import MovieDescription


def prefetch_movie_description(
    movie_slug: str,
) -> MovieDescription:

    movie: MovieDescription | None = next(
        (movie for movie in MOVIES if movie.slug == movie_slug),
        None,
    )
    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug {movie_slug!r} not found",
    )
