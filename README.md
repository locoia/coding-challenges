# gistapi

Gistapi is a simple HTTP API server implemented in Flask for searching a user's public Github Gists.

## Challenge

The existing code already implements most of the Flask boilerplate for you.
The main functionality is left for you to implement.
The goal is to implement an endpoint that searches a user's Gists with a regular expression.
For example, I'd like to know all Gists for user `justdionysus` that contain the pattern `import requests`.
There is also a failing test that should pass once you've successfully implemented the search process (and should illustrate the expected format of the response).
The code in `gistapi.py` contains some comments to help you find your way.

To complete the challenge, you'll have to write some HTTP queries from `Gistapi` to the Github API to pull down each Gist for the target user.
Please don't use a github API client (i.e. using a basic HTTP library like requests or aiohttp or urllib3 is fine but not PyGithub or similar).

Depending on the position you are intereviewing for, we have different sets of additional requirements.
Please, read the section below that is relevant for you, and do not hesitate to ask any questions.
It is expected, however, that you should be able to finish the challenge in about 1.5 hours.
If you feel you are not able to implement everything on time, please, try instead describing how you would solve the points you didn't finish.

## Additional Requirements for Senior Developers

* Implement a few tests (using a testing framework of your choice)
* In all places where it makes sense, implement data validation, error handling, pagination
* Migrate from `requirements.txt` to `pyproject.toml` (e.g. using [poetry](https://python-poetry.org/))
* Implement a simple Dockerfile
* (optionally) Implement handling of huge gists
* (optionally) Set up the necessary tools to ensure code quality (feel free to pick up a set of tools you personally prefer)
* Document how to start the application, how to build the docker image, how to run tests, and (optionally) how to run code quality checkers
* (optionally) Prepare a TODO.md file describing possible further improvements to the archtiecture:
    - Can we use a database? What for? SQL or NoSQL?
    - How can we protect the api from abusing it?
    - How can we deploy the application in a cloud environment?
    - How can we be sure the application is alive and works as expected when deployed into a cloud environment?
    - Any other topics you may find interesting and/or important to cover


## Notes from Caleb:

- Create VENV:
   python3.9 -m venv gist

- Activate VENV
   source gist/bin/activate

- Install:
   pip install poertry
   poetry install

- Lint:
    black src/
    flake8 src/
    isort src/
     
- Run Tests:
  - pytest -s -vv test/

- Build and Run
 -./build.sh (linux or osx)



