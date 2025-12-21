import random
import string

from fastapi import status
from fastapi.testclient import TestClient
from pydantic import AnyHttpUrl

from main import app
from schemas.movies import Movie, MovieCreate


def test_create_movie(auth_client: TestClient) -> None:
    url = app.url_path_for("create_movie")
    movie_create = MovieCreate(
        title="Slug",
        description="SlugSlugSlug",
        genre="Slug",
        year=2020,
        director="Slug Slug",
        rating=8.0,
        url=AnyHttpUrl("https://www.example.com"),
        slug="".join(random.choices(string.ascii_letters, k=8)),
    )
    data: dict[str, str] = movie_create.model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_values = MovieCreate(**response_data)
    assert received_values == movie_create, response_data


def test_create_movie_already_exists(auth_client: TestClient, movie: Movie) -> None:
    movie_create = MovieCreate(**movie.model_dump())
    data: dict[str, str] = movie_create.model_dump(mode="json")
    url = app.url_path_for("create_movie")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_data = response.json()
    expected_error_detail = f"Movie with slug {movie.slug!r} already exists"
    assert response_data["detail"] == expected_error_detail, response_data
