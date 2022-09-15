import os

from flask import Flask
from werkzeug.exceptions import HTTPException

from gistapi.api import search
from gistapi.error import handle_exception
from gistapi.rate_limit import limiter

"""A package implementing the gistapi HTTP API server with Flask."""


"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

app_settings = os.getenv("APP_SETTINGS", "gistapi.config.Development")


def create_app():
    app = Flask(__name__)
    app.config.from_object(app_settings)
    limit = limiter(app)

    @app.route("/ping")
    @limit.limit("2/minute")
    def ping():
        return "pong"

    @app.route("/")
    @limit.limit("10/minute")
    def index():
        return {"version": "0.1.0"}

    @app.route("/api/v1/search", methods=["POST"])
    @limit.limit("3/minute")
    def _searc():
        return search()

    app.register_error_handler(HTTPException, handle_exception)

    return app


def main():
    app = create_app()
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=app.config["PORT"])
