import logging

from fastapi import (
    HTTPException,
    status,
    BackgroundTasks,
)

from schemas.movies import Movie
from .crud import storage

logger = logging.getLogger(__name__)


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


def save_storage_state(
    background_tasks: BackgroundTasks,
):

    yield
    background_tasks.add_task(storage.save_state)
    logger.info("Add background task to save storage.")
