FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_DEBUG 0
ENV FLASK_APP gistapi/gistapi.py

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.7.0

# Configure Poetry
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Copy pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock* /app/

# Installing only main (production) dependencies
RUN poetry install --only main --no-interaction --no-ansi

# Copy application files
COPY gistapi /app/gistapi

# Copy application files
COPY tests /app/tests

# Run the application using Gunicorn with Uvicorn workers
CMD ["gunicorn", "gistapi:asgi_app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:5000"]

