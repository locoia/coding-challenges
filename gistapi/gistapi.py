"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

import re

import requests
from flask import Flask, jsonify, request

from utils import gists_for_user, gist_content, is_pattern_present

app = Flask(__name__)


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


@app.route("/api/v1/search", methods=["POST"])
def search():
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """
    post_data = request.get_json()
    # Validate input data
    if not post_data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    username = post_data.get("username")
    pattern = post_data.get("pattern")
    # Validate username and pattern
    if not username or not isinstance(username, str):
        return (
            jsonify({"status": "error", "message": "Invalid or missing username"}),
            400,
        )
    if not pattern or not isinstance(pattern, str):
        return (
            jsonify({"status": "error", "message": "Invalid or missing pattern"}),
            400,
        )

    result = {
        "status": "success",
        "username": username,
        "pattern": pattern,
        "matches": [],
    }

    try:
        gists = gists_for_user(username)
    except requests.RequestException as e:
        return (
            jsonify({"status": "error", "message": f"Error fetching gists: {e}"}),
            500,
        )

    if gists is None:
        result["status"] = "error"
        result["message"] = (
            "Failed to fetch gists. Please check the username and try again."
        )
        return jsonify(result), 400

    for gist in gists:
        try:
            gist_details = gist_content(gist["url"])
            if gist_details is None:
                continue

            for file_name, file_info in gist_details["files"].items():
                if is_pattern_present(file_info["raw_url"], pattern):
                    result["matches"].append(
                        {
                            "gist_id": gist_details["id"],
                            "gist_url": gist_details["html_url"],
                            "file_name": file_name,
                            "file_url": file_info["raw_url"],
                        }
                    )
        except requests.RequestException as e:
            return (
                jsonify(
                    {"status": "error", "message": f"Error fetching gist content: {e}"}
                ),
                500,
            )

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9876)
