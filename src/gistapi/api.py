import re
import typing

import requests
from flask import abort, jsonify, request
from pydantic.error_wrappers import ValidationError

from .request_schema import Paging, RequestSchema, ResponseSchema


def url_service(*args, **kwargs):
    try:
        resp = requests.get(*args, **kwargs)
        return resp
    except requests.exceptions.RequestException as e:
        print(e)
        abort(422)


def gists_for_user(username: str, parameters: typing.Dict):
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
    gists_url = "https://api.github.com/users/{username}/gists".format(
        username=username
    )
    response = url_service(gists_url, params=parameters)
    return response.json()


def search():
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """
    try:
        request_schema = RequestSchema(payload=request.get_json(), args=request.args)
        gists = gists_for_user(
            request_schema.payload.username, {"per_page": request_schema.args.per_page}
        )
        data = []
        for gist in gists:
            file_key = next(iter(gist["files"].keys()))
            raw_file = gist["files"][file_key]["raw_url"]
            response = url_service(raw_file)
            rc = re.compile((r"[\w\s\ ]{}").format(request_schema.payload.pattern))
            if re.findall(rc, response.text):
                data.append(raw_file)

        results = ResponseSchema(
            status="success",
            username=request_schema.payload.username,
            pattern=request_schema.payload.pattern,
            matches=data,
            pagination=Paging(
                total=len(gists),
                per_page=request_schema.args.per_page,
                page=request_schema.args.page,
            ),
        )

        return jsonify(results.dict())
    except ValidationError as ex:
        print(ex)
        abort(400, description="missing or bad request")
