import logging

import uvicorn
from fastapi import (
    FastAPI,
)

from api import router as api_router
from api.main_views import router as main_router
from app_lifespan import lifespan
from core import config

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI(
    title="Movie Catalog",
    lifespan=lifespan,
)

app.include_router(api_router)
app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
