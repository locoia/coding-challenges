"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

import json
import logging
import os
import re
from asgiref.wsgi import WsgiToAsgi
from http import HTTPStatus

import aiohttp
from flask import Flask, current_app, jsonify, request
from pydantic import ValidationError

from .models import SearchRequest, SearchResult
from .utils import fetch_gists

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)


app = Flask(__name__)


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


@app.route("/api/v1/search", methods=['POST'])
async def search():
    # Extracts the base URL for GitHub's Gist API from environment variables,
    # which allows for configuration flexibility across different deployment environments.
    GISTS_URL = os.getenv("GISTS_URL", "https://api.github.com/users/")

    try:
        post_data = request.get_json()
        # Validate incoming JSON data against the Pydantic model to ensure it conforms to expected structure.
        search_request = SearchRequest(**post_data)
        compiled_pattern = re.compile(search_request.pattern)
    except ValidationError as e:
        # Handles cases where the input does not match the expected schema, logging the error for traceability.
        current_app.logger.error(f"Validation error: {e.errors()}")
        return (
            jsonify({"status": "error", "message": e.errors()}),
            HTTPStatus.BAD_REQUEST,
        )
    except (json.JSONDecodeError, KeyError) as e:
        # Catches issues with JSON decoding or missing fields, indicating the client sent malformed data.
        current_app.logger.error(f"Invalid request data: {e}")
        return (
            jsonify({"status": "error", "message": "Invalid request data"}),
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )
    except re.error as e:
        # Handles invalid regex patterns, which are user input errors.
        current_app.logger.error(f"Regex pattern error: {e}")
        return (
            jsonify({"status": "error", "message": "Invalid regex pattern"}),
            HTTPStatus.BAD_REQUEST,
        )

    async with aiohttp.ClientSession() as session:
        gists_url = f"{GISTS_URL}{search_request.username}/gists"
        try:
            # Asynchronously fetches gists and filters them by the regex pattern provided.
            matches = await fetch_gists(
                session, gists_url, compiled_pattern, logger=current_app.logger
            )
        except RuntimeError as e:
            # Handles exceptions such as rate limits from the GitHub API,
            # communicating service unavailability to the client.
            current_app.logger.error(f"Runtime error: {e}")
            return (
                jsonify({"status": "error", "message": str(e)}),
                HTTPStatus.SERVICE_UNAVAILABLE,
            )
        except aiohttp.ClientError as e:
            # Captures any HTTP errors encountered during API interaction.
            status_code = (
                e.status if hasattr(e, "status") else HTTPStatus.INTERNAL_SERVER_ERROR
            )
            return jsonify({"status": "error", "message": str(e)}), status_code

    # Successfully returns search results wrapped in a SearchResult model.
    result = SearchResult(
        status="success",
        username=search_request.username,
        pattern=search_request.pattern,
        matches=matches,
    )
    return jsonify(result.dict())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9876)
