import logging

from fastapi import (
    FastAPI,
    Request,
)

import uvicorn

from api import router as api_router
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


@app.get("/")
def get_docs(
    request: Request,
):
    docs_url = request.url.replace(
        path="/docs",
    )
    return {
        "docs": str(docs_url),
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )
