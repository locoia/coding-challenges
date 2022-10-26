"""
Exposes a simple HTTP API to search a users Gists via a regular expression.
Github provides the Gist service as a pastebin analog for sharing code and
other development artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

import re
import requests
import requests_cache

from flask import Flask, jsonify, request
from requests_cache import CachedSession
from datetime import timedelta

app = Flask(__name__)

# Caching

requests_cache.install_cache('gistapi2_cache')
session = CachedSession(
    'gistapi2_cache',
    use_cache_dir=True,
    cache_control=True,
    expire_after=timedelta(days=1),
    allowable_methods=['GET'],
    allowable_codes=[200],
    ignored_parameters=['api_key'],
    match_headers=True,
    stale_if_error=True,
)


# Error Handling, Validation and Formatting

def success_response(username, pattern, matches):
    result = {
        'status': 'success',
        'username': username,
        'pattern': pattern,
        'matches': matches,
    }
    return jsonify(result)


def pagination(matched_gists, page, per_page):
    if not matched_gists:
        return matched_gists
    start = (page - 1) * per_page
    end = page * per_page
    print(start, end)
    return matched_gists[start:end]


def validate_data(data):
    validate_alpha_numeric = re.compile("^[a-zA-Z0-9]*_?[a-zA-Z0-9]*$")
    if validate_alpha_numeric.match(data):
        return True
    return False


def error_verification(message, code):
    result = {
        'status': 'error',
        'message': message
    }
    return jsonify(result), code


def validate_regex(data):
    try:
        re.compile(data)
        return True
    except re.error:
        return False


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


def gists_for_user(username):
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
    gists_url = 'https://api.github.com/users/{username}/gists'.format(username=username)

    # Testing server connection for errors
    try:
        response = requests.get(gists_url)
        return response.json()
    except:
        return error_verification('connecting to server in Error', 500)


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

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per-page", 5, type=int)
    post_data = request.get_json()
    username = post_data['username']
    pattern = post_data['pattern']

    # Command Error Validation

    if not username:
        return error_verification('no username provided', 400)

    if not pattern:
        return error_verification('no pattern provided', 400)

    gists = gists_for_user(username)

    count = 0
    matched = []
    for gist in gists:
        gist_files = list(gist['files'].keys())
        file_url = gist['files'][gist_files[0]]['raw_url']
        opened_url = requests.get(file_url)

        opened_url_to_string = opened_url.content.decode('utf-8')
        if re.search(pattern, opened_url_to_string):
            public_gist_url = "https://gist.github.com/" + username + "/" + gist['id']
            matched.append(public_gist_url)
        count = count + 1
        pass

    return success_response(username, pattern, pagination(matched, page, per_page))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9876)
