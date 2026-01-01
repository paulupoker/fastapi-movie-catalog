from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.movies.crud import storage
from main import app
from schemas.movies import DESCRIPTION_MAX_LENGTH, Movie
from testing.conftest import create_movie_random_slug


class TestUpdatePartial:
    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie]:
        movie = create_movie_random_slug(request.param)
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_description",
        [
            pytest.param(
                "description",
                "",
                id="text_description_to_empty_description",
            ),
            pytest.param(
                "",
                "description",
                id="empty_description_to_text_description",
            ),
            pytest.param(
                "a" * DESCRIPTION_MAX_LENGTH,
                "",
                id="max_description_to_empty_description",
            ),
            pytest.param(
                "",
                "a" * DESCRIPTION_MAX_LENGTH,
                id="empty_description_to_max_description",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details_partial(
        self, movie: Movie, new_description: str, auth_client: TestClient
    ) -> None:
        url = app.url_path_for("update_movie_details_partial", slug=movie.slug)
        new_description = movie.description
        response = auth_client.patch(url, json={"description": new_description})
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_db = storage.get_by_slug(movie.slug)
        assert movie_db
        assert movie_db.description == new_description
