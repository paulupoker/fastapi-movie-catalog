import random
import string
from collections.abc import Generator
from os import getenv

import pytest
from pydantic import AnyHttpUrl

from api.api_v1.movies.crud import storage
from schemas.movies import Movie, MovieCreate

if getenv("TESTING") != "1":
    pytest.exit("Environment is not ready for testing.")


def build_movie_create(slug: str) -> MovieCreate:
    return MovieCreate(
        title="Slug",
        description="Description",
        genre="Genre",
        year=2020,
        director="Director Director",
        rating=8.0,
        url=AnyHttpUrl("https://www.example.com"),
        slug=slug,
    )


def build_movie_create_random_slug() -> MovieCreate:
    return build_movie_create(
        slug="".join(random.choices(string.ascii_letters, k=8)),
    )


def create_movie(slug: str) -> Movie:
    movie_in = build_movie_create(slug)
    return storage.create(movie_in)


def create_movie_random_slug() -> Movie:
    movie_in = build_movie_create_random_slug()
    return storage.create(movie_in)


@pytest.fixture()
def movie() -> Generator[Movie]:
    movie = create_movie_random_slug()
    yield movie
    storage.delete(movie)
