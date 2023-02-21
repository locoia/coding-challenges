## Prerequisites
  - Python 3.8
  - Poetry package manager
  - Docker, if intending to use docker container

## Setup
  - in the root folder of the project run `poetry install`

## Running the service

The service can be run in 2 ways:
  - by running `flask --app ./gistapi/gistapi run --host=0.0.0.0`
  - or by running a docker container `docker build -t gistapi . && docker run -it gistapi`
  
In order to run tests, this command should be run in terminal: `poetry run pytest`

For code quality checks, run pylint with this command: `poetry run pylint gistapi` or 
    `poetry run pylint --load-plugins pylint_flask gistapi` to use flask specific linter.
