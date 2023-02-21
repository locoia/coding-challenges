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
from constants import constants


app = Flask(__name__)


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


def gists_for_user(username: str):
    """Provides the list of gist metadata for a given user.

    This abstracts the /users/:username/gist endpoint from the Github API.
    See https://developer.github.com/v3/gists/#list-a-users-gists for
    more information.

    Args:
        username (string): the user to query gists for

    Returns:
        The dict parsed from the json response from the Github API.  See
        the above URL for details of the expected structure.
    """
    gists_url = f'https://api.github.com/users/{username}/gists'
    response = requests.get(gists_url, timeout=10)
    return response.json()


def gist_file_data(gist_url: str):
    """Returns gist file content
        Args:
            gist_url (string): the gist file raw url

        Returns:
            Raw bytes of the gist file retrieved. If retrieval failed, returns empty bytes
    """
    response = requests.get(gist_url, timeout=10)
    return response.content


def find_match_in_gist(gist_url: str, pattern: re.Pattern):
    """Finds a match within gist of specified url with specified pattern
        Args:
            gist_url (string): the gist file raw url
            pattern (re.Pattern): Pattern object of re library

        Returns:
            Pattern object of re library, if a match is found, otherwise returns None
    """
    match = None
    with requests.get(gist_url, stream=True, timeout=10) as gist:
        lines = gist.iter_lines()
        for line in lines:
            match = re.search(pattern, line)
            if match:
                break
        return match


@app.route("/api/v1/search", methods=['POST'])
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

    username = post_data['username']
    pattern = post_data['pattern']

    if username == "":
        return jsonify({"status": constants.STATUS_ERROR, "error": constants.ERROR_NO_USERNAME})

    if pattern == "":
        return jsonify({"status": constants.STATUS_ERROR, "error": constants.ERROR_NO_PATTERN})

    try:
        regex_compiled = re.compile(pattern.encode('utf-8'))
    except re.error:
        return jsonify({"status": constants.STATUS_ERROR, "error": constants.ERROR_INVALID_PATTERN})

    result = {}
    try:
        gists = gists_for_user(username)
    except (requests.RequestException, requests.JSONDecodeError):
        return jsonify({"status": constants.STATUS_ERROR,
                        "error": constants.ERROR_FAILED_FETCH_GISTS})

    errors = []
    matches = []
    for gist in gists:
        for file in gist['files']:
            raw_url = gist['files'][file]['raw_url']
            # with file
            try:
                # since the filesize is known from the list,
                # can choose a method to handle large files with streaming
                if gist['files'][file]['size'] > constants.ONEMB_IN_BYTES:
                    match = find_match_in_gist(raw_url, regex_compiled)
                else:
                    fetched_gist = gist_file_data(raw_url)
                    match = re.search(regex_compiled, fetched_gist)
                if match:
                    matches.append(
                        {
                            "gist_url": gist['url'],
                            "filename": file,
                            "raw_url": raw_url,
                        }
                    )
            except requests.RequestException:
                errors.append({"status": constants.STATUS_ERROR,
                               "error": constants.ERROR_FAILED_FETCH_GIST})

    if len(errors) > 0:
        return jsonify({"errors": errors})

    result['status'] = constants.STATUS_SUCCESS
    result['username'] = username
    result['pattern'] = pattern
    result['matches'] = matches

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9876)
