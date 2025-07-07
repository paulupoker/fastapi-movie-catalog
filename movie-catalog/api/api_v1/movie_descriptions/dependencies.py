from fastapi import (
    HTTPException,
    status,
)

from schemas.movies import Movie
from .crud import storage


def prefetch_movie(
    slug: str,
) -> Movie:

    movie: Movie | None = storage.get_by_slug(slug=slug)
    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug {slug!r} not found",
    )
