from unittest import TestCase

from pydantic import AnyHttpUrl, ValidationError

from schemas.movies import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)


class MovieCreateTestCase(TestCase):
    def test_movie_can_be_created(self) -> None:
        movie_in = MovieCreate(
            slug="test_movie",
            title="Test Movie",
            description="Test description",
            genre="Test genre",
            year=2025,
            director="DirectorString",
            rating=8.0,
            url=AnyHttpUrl("https://www.example.com"),
        )

        movie = Movie(**movie_in.model_dump())

        self.assertEqual(movie_in.slug, movie.slug)
        self.assertEqual(movie_in.title, movie.title)
        self.assertEqual(movie_in.description, movie.description)
        self.assertEqual(movie_in.genre, movie.genre)
        self.assertEqual(movie_in.year, movie.year)
        self.assertEqual(movie_in.director, movie.director)
        self.assertEqual(movie_in.rating, movie.rating)
        self.assertEqual(movie_in.url, movie.url)

    def test_movie_create_accepts_different_titles_lengths(self) -> None:
        titles = [
            "Test Movie",
            "TTT",
            "T" * 100,
        ]

        for title in titles:
            with self.subTest(title=title):
                movie_create = MovieCreate(
                    slug="test_movie",
                    title=title,
                    description="Test description",
                    genre="Test genre",
                    year=2025,
                    director="DirectorString",
                    rating=8.0,
                    url=AnyHttpUrl("https://www.example.com"),
                )

                self.assertEqual(title, movie_create.title)

    def test_movie_slug_too_short(self) -> None:
        with self.assertRaises(ValidationError) as exc_info:
            MovieCreate(
                slug="t",
                title="Test Movie",
                description="Test description",
                genre="Test genre",
                year=2025,
                director="DirectorString",
                rating=8.0,
                url=AnyHttpUrl("https://www.example.com"),
            )

        error_details = exc_info.exception.errors()[0]
        expected_errors = "string_too_short"

        self.assertEqual(
            expected_errors,
            error_details["type"],
        )

    def test_movie_slug_too_short_with_regex(self) -> None:
        with self.assertRaisesRegex(
            ValidationError,
            expected_regex="String should have at least 2 characters",
        ):
            MovieCreate(
                slug="t",
                title="Test Movie",
                description="Test description",
                genre="Test genre",
                year=2025,
                director="DirectorString",
                rating=8.0,
                url=AnyHttpUrl("https://www.example.com"),
            )


class MovieUpdateTestCase(TestCase):
    def test_movie_can_be_updated(self) -> None:
        movie_in = MovieUpdate(
            title="Test Movie",
            description="Test description",
            genre="Test genre",
            year=2025,
            director="DirectorString",
            rating=8.0,
            url=AnyHttpUrl("https://www.example.com"),
        )

        movie = Movie(slug="test_movie", **movie_in.model_dump())

        self.assertEqual(movie_in.title, movie.title)
        self.assertEqual(movie_in.description, movie.description)
        self.assertEqual(movie_in.genre, movie.genre)
        self.assertEqual(movie_in.year, movie.year)
        self.assertEqual(movie_in.director, movie.director)
        self.assertEqual(movie_in.rating, movie.rating)
        self.assertEqual(movie_in.url, movie.url)


class MoviePartialUpdateTestCase(TestCase):
    def test_movie_can_be_partial_updated(self) -> None:
        movie_in = MoviePartialUpdate(
            description="Test description",
        )

        movie = Movie(
            slug="test_movie",
            title="Test Movie",
            description="Test description",
            genre="Test genre",
            year=2025,
            director="DirectorString",
            rating=8.0,
            url=AnyHttpUrl("https://www.example.com"),
        )

        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)

        if not movie_in.model_dump(exclude_unset=True).keys():
            self.assertEqual("Test description", movie.description)
        else:
            self.assertEqual(movie_in.description, movie.description)
