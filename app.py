import re

from flask import Flask, jsonify, request

from gistapi import is_matching_gist, gists_for_user

app = Flask(__name__)


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


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

    # TODO Pydantic models could be used here
    username = post_data.get('username')
    pattern = post_data.get('pattern')
    if username is None or pattern is None:
        return jsonify({'error': 'Please username and pattern'}), 400

    result = {
        'status': 'success', 'username': username, 'pattern': pattern, 'matches': []
    }

    try:
        regex_pattern = re.compile(pattern)
    except Exception:
        return jsonify({'error': 'Please provide a valid regex pattern'}), 400

    gists = gists_for_user(username)
    for gist in gists:  # TODO this could be a nice list comprehension, but debugging would be harder
        if is_matching_gist(gist, regex_pattern):
            result['matches'].append(gist)

    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9876)
