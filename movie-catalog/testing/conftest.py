import random
import string
from collections.abc import Generator
from os import getenv

import pytest
from pydantic import AnyHttpUrl

from api.api_v1.movies.crud import storage
from schemas.movies import Movie, MovieCreate


@pytest.fixture(scope="session", autouse=True)
def check_testing_env() -> None:
    if getenv("TESTING") != "1":
        pytest.exit("Environment is not ready for testing.")


def build_movie_create(
    slug: str, title: str = "Title", description: str = "Description"
) -> MovieCreate:
    return MovieCreate(
        title=title,
        description=description,
        genre="Genre",
        year=2020,
        director="Director Director",
        rating=8.0,
        url=AnyHttpUrl("https://www.example.com"),
        slug=slug,
    )


def build_movie_create_random_slug(
    title: str = "Title", description: str = "Description"
) -> MovieCreate:
    return build_movie_create(
        slug="".join(random.choices(string.ascii_letters, k=8)),
        title=title,
        description=description,
    )


def create_movie(
    slug: str, title: str = "Title", description: str = "Description"
) -> Movie:
    movie_in = build_movie_create(slug, title=title, description=description)
    return storage.create(movie_in)


def create_movie_random_slug(
    title: str = "Title", description: str = "Description"
) -> Movie:
    movie_in = build_movie_create_random_slug(title=title, description=description)
    return storage.create(movie_in)


@pytest.fixture()
def movie() -> Generator[Movie]:
    movie = create_movie_random_slug()
    yield movie
    storage.delete(movie)
