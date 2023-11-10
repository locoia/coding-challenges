FROM python:3.11-slim-buster

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false \
  && poetry install --no-root --no-directory

COPY . /app

RUN poetry install

EXPOSE 9876

CMD ["flask", "run"]
