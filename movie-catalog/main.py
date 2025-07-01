from fastapi import (
    FastAPI,
    Request,
)

import uvicorn

from api import router as api_router

app = FastAPI(
    title="Movie Catalog",
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
