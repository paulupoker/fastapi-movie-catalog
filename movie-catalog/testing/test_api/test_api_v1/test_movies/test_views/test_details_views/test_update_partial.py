from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.movies.crud import storage
from main import app
from schemas.movies import (
    DESCRIPTION_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    TITLE_MIN_LENGTH,
    Movie,
)
from testing.conftest import create_movie_random_slug


class TestUpdatePartial:
    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie]:
        title, description = request.param
        movie = create_movie_random_slug(title=title, description=description)
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_title, new_description",
        [
            pytest.param(
                ("some_title", "some_description"),
                "some_title",
                "some_description",
                id="some_params",
            ),
            pytest.param(
                ("old_title", "old_description"),
                "new_title",
                "new_description",
                id="new_params",
            ),
            pytest.param(
                ("new_title", "new_description"),
                "a" * TITLE_MIN_LENGTH,
                "",
                id="min_params",
            ),
            pytest.param(
                ("a" * TITLE_MIN_LENGTH, ""),
                "a" * TITLE_MAX_LENGTH,
                "a" * DESCRIPTION_MAX_LENGTH,
                id="max_params",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details_partial(
        self,
        movie: Movie,
        new_title: str,
        new_description: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("update_movie_details_partial", slug=movie.slug)
        new_title = movie.title
        new_description = movie.description
        response = auth_client.patch(
            url, json={"title": new_title, "description": new_description}
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_db = storage.get_by_slug(movie.slug)
        assert movie_db
        assert movie_db.description == new_description
