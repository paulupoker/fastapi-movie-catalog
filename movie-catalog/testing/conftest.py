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


def create_movie() -> Movie:
    movie_in = MovieCreate(
        title="Slug",
        description="SlugSlugSlug",
        genre="Slug",
        year=2020,
        director="Slug Slug",
        rating=8.0,
        url=AnyHttpUrl("https://www.example.com"),
        slug="".join(random.choices(string.ascii_letters, k=8)),
    )
    return storage.create(movie_in)


@pytest.fixture()
def movie() -> Generator[Movie]:
    movie = create_movie()
    yield movie
    storage.delete(movie)
