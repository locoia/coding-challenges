"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

import asyncio
import re
from http import HTTPStatus

import aiohttp
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
logger = app.logger


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


def gists_for_user(username: str) -> dict:
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
    gists_url = f"https://api.github.com/users/{username}/gists"
    response = requests.get(gists_url)

    if response.status_code != HTTPStatus.OK:
        response.raise_for_status()

    return response.json()


async def _fetch_content(raw_file_url: str) -> str:
    """Fetch the content of the file at the given URL.

    Args:
        raw_file_url (str): The URL of the file to fetch.

    Returns:
        The content of the file.

    Raises:
        aiohttp.ClientError: If there was an error fetching the file.
        Exception: If there was an error reading the file content.
    """
    async with aiohttp.ClientSession() as session, session.get(raw_file_url) as response:
        if response.status != HTTPStatus.OK:
            raise aiohttp.ClientError(f"Error fetching {raw_file_url}: {response.status} {response.reason}")
        return await response.text()


def _matches_pattern(content: str, pattern: str) -> bool:
    """Check if the given content matches the given pattern.

    Args:
        content (str): The content to check.
        pattern (str): The pattern to match.

    Returns:
        A boolean indicating whether the pattern matched the content.
    """
    return bool(re.search(pattern, content))


async def fetch_and_check_pattern(raw_file_url: str, pattern: str) -> bool:
    """Fetch the content of the file at the given URL and check if it matches the given pattern.

    Args:
        raw_file_url (str): The URL of the file to fetch.
        pattern (str): The pattern to match in the file content.

    Returns:
        A boolean indicating whether the pattern matched the content.

    Raises:
        aiohttp.ClientError: If there was an error fetching the file.
        Exception: If there was an error reading the file content.
    """
    try:
        content = await _fetch_content(raw_file_url)
        return _matches_pattern(content, pattern)
    except Exception as e:
        logger.error(f"Error during fetching and matching of pattern: {e}")
        raise


async def find_matching_gists(gists: dict, pattern: str) -> list[str]:
    """
    Finds all gists that contain at least one file matching the given pattern.

    Args:
        gists (dict): A dictionary of gists to search through.
        pattern (str): The pattern to search for in the gist files.

    Returns:
        A list of URLs for all gists that contain at least one file matching the pattern.
    """
    gist_matches = []
    for gist in gists:
        tasks = []
        try:
            async with asyncio.TaskGroup() as tg:
                for file_obj in gist["files"].values():
                    raw_file_url = file_obj["raw_url"]
                    tasks.append(tg.create_task(fetch_and_check_pattern(raw_file_url, pattern)))
        except Exception as e:
            logger.error(f"Error fetching gist {gist['html_url']}: {e}")
            continue

        for task in tasks:
            if task.result() is True:
                gist_matches.append(gist["html_url"])
                break

    return gist_matches


@app.route("/api/v1/search", methods=["POST"])
async def search():
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """
    post_data = request.get_json()

    username = post_data["username"]
    pattern = post_data["pattern"]

    result = {"status": "success", "username": username, "pattern": pattern, "matches": []}

    try:
        gists = gists_for_user(username)
    except requests.HTTPError as e:
        result["status"] = str(e)
        return jsonify(result), e.response.status_code

    try:
        result["matches"] = await find_matching_gists(gists, pattern)
    except Exception as e:
        result["status"] = str(e)
        return jsonify(result), HTTPStatus.INTERNAL_SERVER_ERROR

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9876)
