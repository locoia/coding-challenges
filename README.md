# gistapi

Gistapi is a simple HTTP API server implemented in Flask for searching a user's public Github Gists.


## Notes from Caleb:

- Create VENV:
   - python3.9 -m venv gist

- Activate VENV
   - source gist/bin/activate

- Install:
   - pip install poertry
   - poetry install

- Lint:
    - black src/
    - flake8 src/
    - isort src/
     
- Run Tests:
  - pytest -s -vv test/

- Build and Run
  - ./build.sh (linux or osx)

- Change Env
  - export APP_SETTINGS="gistapi.config.Production"

