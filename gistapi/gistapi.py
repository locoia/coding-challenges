"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

import requests
from flask import Flask, jsonify, request
from flask_restful import Api

from resources.search import GistSearchApi


app = Flask(__name__)
api = Api(app)


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


api.add_resource(GistSearchApi, "/api/v1/search", endpoint="search")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9876)
