import logging

from pydantic import (
    BaseModel,
)
from redis import Redis

from core import config
from schemas.movies import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)

logger = logging.getLogger(__name__)


redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES,
    decode_responses=True,
)


class MovieBaseError(Exception):
    """
    Base exception for movie CRUD actions.
    """


class MovieAlreadyExists(MovieBaseError):
    """
    Raised movie creation if such slug already exists.
    """


class MoviesStorage(BaseModel):

    def get(self) -> list[Movie]:
        return [
            Movie.model_validate_json(value)
            for value in redis.hvals(name=config.REDIS_MOVIES_HASH_NAME)
        ]

    def get_by_slug(self, slug: str) -> Movie | None:
        if movie := redis.hget(name=config.REDIS_MOVIES_HASH_NAME, key=slug):
            return Movie.model_validate_json(movie)
        return None

    def exists(self, slug: str) -> bool:
        return bool(
            redis.hexists(
                name=config.REDIS_MOVIES_HASH_NAME,
                key=slug,
            )
        )

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

    def create_or_raise_if_exists(self, movie_in: MovieCreate) -> Movie:
        if not self.exists(movie_in.slug):
            return self.create(movie_in)
        raise MovieAlreadyExists(movie_in.slug)

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
