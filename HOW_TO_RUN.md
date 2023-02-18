## How To Run?

### Used tech stacks

* python3.9 - main programming language
* requests - library for requesting gists
* poetry - packaging manager tool
* docker - docker compose
* pytest - unit testing
* pylint and flake8 - code quality and formatting

### Configure environment

* Create python virtual environment
In the project folder create a virtual python environment with the following command: `python -m venv env`

* Install libraries and dependencies
After creating the virtual environment, enable the environment and install the poetry library first:
`source env/bin/activate`
`pip install poetry`

* Then install all dependencies: `poetry install`

### How to start application

* RUN (docker)  - For starting application in docker: `docker-compose up --build -d`
* RUN (local)   - `poetry run python gistapi/gistapi.py run --host=0.0.0.0 -p 9876`
* RUN (tests)   - `poetry run pytest -v`
* RUN (quality checkers)   - 
  - `export PYTHONPATH="$PWD/gistapi"/`
  - `poetry run flake8 gistapi/` & `poetry run pylint gistapi/`
