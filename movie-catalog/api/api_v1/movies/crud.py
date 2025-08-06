from redis import Redis
from pydantic import (
    BaseModel,
    ValidationError,
)

import logging

from core import config
from core.config import MOVIES_STORAGE_FILEPATH
from schemas.movies import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MoviePartialUpdate,
)

logger = logging.getLogger(__name__)


redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES,
    decode_responses=True,
)


class MoviesStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def save_state(self) -> None:
        MOVIES_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        logger.info("Saved movies to storage file")

    @classmethod
    def from_state(cls) -> "MoviesStorage":
        if not MOVIES_STORAGE_FILEPATH.exists():
            logger.warning("Movies storage file doesn't exist")
            return MoviesStorage()
        return cls.model_validate_json(MOVIES_STORAGE_FILEPATH.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = MoviesStorage.from_state()
        except ValidationError:
            self.save_state()
            logger.warning("Rewritten storage file due to validation error")
            return

        self.slug_to_movie.update(
            data.slug_to_movie,
        )
        logger.warning("Recovered data from storage file")

    def get(self) -> list[Movie]:
        return [
            Movie.model_validate_json(value)
            for value in redis.hvals(name=config.REDIS_MOVIES_HASH_NAME)
        ]

    def get_by_slug(self, slug: str) -> Movie | None:
        if movie := redis.hget(name=config.REDIS_MOVIES_HASH_NAME, key=slug):
            return Movie.model_validate_json(movie)
        return None

    def save_movie(self, movie: Movie) -> None:
        redis.hset(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        self.save_movie(movie)
        logger.info("Created a new movie with slug: %r", movie.slug)
        return movie

    def delete_by_slug(self, slug: str) -> None:
        if redis.hdel(config.REDIS_MOVIES_HASH_NAME, slug):
            logger.info("Deleted the movie with slug: %r", slug)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_movie(movie)
        logger.info("Updated the movie with slug: %r", movie.slug)
        return movie

    def update_partial(
        self,
        movie: Movie,
        movie_in: MoviePartialUpdate,
    ) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_movie(movie)
        logger.info("Partially updated the movie with slug: %r", movie.slug)
        return movie


storage = MoviesStorage()
