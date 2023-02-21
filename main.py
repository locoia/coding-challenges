"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""
from gistapi.env import DEBUG, APP_HOST, APP_PORT

from flask import Flask
from gistapi.api.gists import gists


app = Flask(__name__)


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


app.register_blueprint(gists)

if __name__ == '__main__':
    app.run(debug=DEBUG, host=APP_HOST, port=APP_PORT)
