# Use the official Python runtime as a parent image
FROM python:3.12.4-slim-bullseye

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry==1.7.1

# Copy only the dependency files first to leverage Docker cache
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Set the FLASK_APP environment variable
ENV FLASK_APP=gistapi/gistapi.py

# Copy the rest of the application code
COPY . /app/

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask app using Poetry
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]
