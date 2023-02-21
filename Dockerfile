FROM python:3.8-alpine3.17

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry install --no-interaction

COPY . /app

CMD ["poetry", "run", "flask", "--app", "./gistapi/gistapi", "run", "--host=0.0.0.0"]
