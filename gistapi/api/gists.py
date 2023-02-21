from flask import request, jsonify, Blueprint
from requests import HTTPError

from gistapi.api import URL_PREFIX
from gistapi.utils.gist_utils import get_matched_gists
from gistapi.exceptions import UserNotFound, InvalidPayload

gists = Blueprint('gists', __name__, url_prefix=URL_PREFIX)


@gists.route("/search", methods=['POST'])
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

    username = post_data.get('username')
    pattern = post_data.get('pattern')
    try:
        user_gists = get_matched_gists(username, pattern)
        result = {
            'username': username,
            'pattern': pattern,
            'matches': user_gists,
            'status': 'success',
        }
    except (UserNotFound, HTTPError, InvalidPayload) as e:
        result = {
            'error': str(e),
            'status': 'failed',
        }

    return jsonify(result)
