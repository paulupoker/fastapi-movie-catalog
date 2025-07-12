from fastapi import (
    APIRouter,
    status,
)

from api.api_v1.movies.crud import storage
from schemas.movies import (
    Movie,
    MovieRead,
    MovieCreate,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[MovieRead],
)
def read_movie_list() -> list[Movie]:
    return storage.get()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie: MovieCreate,
) -> Movie:
    return storage.create(movie)
