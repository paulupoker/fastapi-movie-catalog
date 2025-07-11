from pydantic import (
    BaseModel,
    AnyHttpUrl,
)

from schemas.movies import (
    Movie,
    MovieCreate,
    MovieUpdate,
)


class MoviesStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        self.slug_to_movie[movie.slug] = movie
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        return movie


storage = MoviesStorage()

storage.create(
    MovieCreate(
        slug="leon",
        title="Леон",
        description="Профессиональный убийца Леон неожиданно для себя самого "
        "решает помочь 12-летней соседке Матильде, семью которой "
        "убили коррумпированные полицейские.",
        genre="боевик, триллер, драма, криминал",
        year=1994,
        director="Люк Бессон",
        rating=8.7,
        url=AnyHttpUrl("https://www.kinopoisk.ru/film/389/"),
    )
),

storage.create(
    MovieCreate(
        slug="stringer",
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
        url=AnyHttpUrl("https://www.kinopoisk.ru/film/760815/"),
    )
),

storage.create(
    MovieCreate(
        slug="dzhentlmeny",
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
        url=AnyHttpUrl("https://www.kinopoisk.ru/film/1143242/"),
    )
)
