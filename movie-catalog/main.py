from typing import Annotated
from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    Depends,
)
import uvicorn

from schemas.movie_description import MovieDescription

MOVIES = [
    MovieDescription(
        id=1,
        title="Léon",
        description="Профессиональный убийца Леон неожиданно для себя самого "
        "решает помочь 12-летней соседке Матильде, семью которой "
        "убили коррумпированные полицейские.",
        genre="боевик, триллер, драма, криминал",
        year=1994,
        director="Люк Бессон",
        rating=8.7,
    ),
    MovieDescription(
        id=2,
        title="Стрингер",
        description="Луи Блум пытается найти работу. После того как он видит, "
        "как любительская съемочная группа снимает автомобильную "
        "аварию, он меняет ворованный велосипед на камеру и снимает "
        "последствия угона автомобиля, чтобы продать местной телевизионной "
        "компании. Директор новостей Нина покупает запись и убеждает его "
        "продолжить работу. Вскоре становится ясно, что ради по-настоящему "
        "стоящего материала Луи не остановится ни перед чем...",
        genre="триллер, драма, криминал",
        year=2013,
        director="Дэн Гилрой",
        rating=7.4,
    ),
    MovieDescription(
        id=3,
        title="Джентльмены",
        description="Один ушлый американец ещё со студенческих лет приторговывал "
        "наркотиками, а теперь придумал схему нелегального обогащения "
        "с использованием поместий обедневшей английской аристократии "
        "и очень неплохо на этом разбогател. Другой пронырливый журналист "
        "приходит к Рэю, правой руке американца, и предлагает тому купить "
        "киносценарий, в котором подробно описаны преступления его босса "
        "при участии других представителей лондонского криминального "
        "мира — партнёра-еврея, китайской диаспоры, чернокожих спортсменов "
        "и даже русского олигарха.",
        genre="криминал, комедия, боевик",
        year=2019,
        director="Гай Ричи",
        rating=8.6,
    ),
]

app = FastAPI(
    title="Movie Catalog",
)


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


@app.get(
    "/movies/",
    response_model=list[MovieDescription],
)
def read_movie_list():
    return MOVIES


def prefetch_movie_description(
    movie_id: int,
) -> MovieDescription:

    movie: MovieDescription | None = next(
        (movie for movie in MOVIES if movie.id == movie_id),
        None,
    )
    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with id {movie_id} not found",
    )


@app.get("/movies/{id}", response_model=MovieDescription)
def read_movie(
    movie: Annotated[
        MovieDescription,
        Depends(prefetch_movie_description),
    ],
) -> MovieDescription:

    return movie


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )
