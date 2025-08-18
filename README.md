# FastAPI Movie Catalog

## Develop

### Setup

Right click `movie-catalog` -> Mark Directory as -> Sources Root

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```

### Install

Install packages:

```shell
uv install
```

### Run

Go to workdir:

```shell
cd movie-catalog
```

Run dev server:
```shell
fastapi dev
```

## Snippets

```shell
python -c 'import secrets;print(secrets.token_urlsafe(16))'
```
