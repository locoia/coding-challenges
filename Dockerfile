FROM python:3.10.0-slim

RUN pip install --upgrade pip && pip install poetry

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml ./

RUN poetry config virtualenvs.create false  \
    && poetry install --no-interaction --no-ansi

COPY . .
