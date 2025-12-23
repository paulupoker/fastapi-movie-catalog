import pytest
from _pytest.fixtures import SubRequest
from fastapi.testclient import TestClient
from starlette import status

from api.api_v1.movies.crud import storage
from main import app
from schemas.movies import Movie
from testing.conftest import create_movie


@pytest.fixture(
    params=[
        pytest.param("some-slug", id="common slug"),
        pytest.param("abc", id="min length slug"),
        pytest.param("abc" * 10, id="max length slug"),
    ],
)
def movie(request: SubRequest) -> Movie:
    return create_movie(request.param)


def test_delete(movie: Movie, auth_client: TestClient) -> None:
    url = app.url_path_for("delete_movie", slug=movie.slug)
    response = auth_client.delete(url=url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(movie.slug)
