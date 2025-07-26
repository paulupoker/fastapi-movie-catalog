from fastapi import (
    APIRouter,
    status,
    Depends,
)

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import (
    save_storage_state,
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from schemas.movies import (
    Movie,
    MovieRead,
    MovieCreate,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[
        Depends(save_storage_state),
        Depends(api_token_or_user_basic_auth_required_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_token": {
                            "summary": "Invalid API token",
                            "value": {"detail": "Invalid API token"},
                        },
                        "invalid_basic": {
                            "summary": "Invalid username or password",
                            "value": {"detail": "Invalid username or password"},
                        },
                    },
                },
            },
        },
    },
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
def create_movie(movie_create: MovieCreate) -> Movie:
    return storage.create(movie_create)
