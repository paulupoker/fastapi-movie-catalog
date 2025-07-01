from fastapi import APIRouter

from .movie_descriptions.views import router as movie_descriptions_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(movie_descriptions_router)
