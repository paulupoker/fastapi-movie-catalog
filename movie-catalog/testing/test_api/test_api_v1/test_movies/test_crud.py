import random
import string
from os import getenv
from unittest import TestCase

from pydantic import AnyHttpUrl

from api.api_v1.movies.crud import storage
from schemas.movies import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)

if getenv("TESTING") != "1":
    msg = "Environment is not ready for testing."
    raise OSError(msg)


class MoviesStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = self.create_movie()

    def tearDown(self) -> None:
        storage.delete(self.movie)

    def create_movie(self) -> Movie:
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

    def test_update(self) -> None:
        movie_update = MovieUpdate(**self.movie.model_dump())
        source_description = self.movie.description
        movie_update.description *= 2
        updated_movie = storage.update(
            movie=self.movie,
            movie_in=movie_update,
        )
        self.assertNotEqual(
            source_description,
            updated_movie.description,
        )
        self.assertEqual(
            movie_update,
            MovieUpdate(**updated_movie.model_dump()),
        )

    def test_update_partial(self) -> None:
        movie_partial_update = MoviePartialUpdate(
            description=self.movie.description * 2,
        )
        source_description = self.movie.description
        updated_movie = storage.update_partial(
            movie=self.movie,
            movie_in=movie_partial_update,
        )
        self.assertNotEqual(
            source_description,
            updated_movie.description,
        )
        self.assertEqual(
            movie_partial_update.description,
            updated_movie.description,
        )
