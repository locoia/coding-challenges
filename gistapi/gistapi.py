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
    gists_url = "https://api.github.com/users/{username}/gists".format(username=username)
    response = requests.get(gists_url)
    return response.json()


async def fetch_and_match(raw_file_url: str, pattern: str) -> bool:
    """Fetch the content of the file at the given URL and check if it matches the given pattern.

    Args:
        raw_file_url (str): The URL of the file to fetch.
        pattern (str): The pattern to match in the file content.

    Returns:
        A boolean indicating whether the file content matched the given pattern.
    """
    try:
        async with aiohttp.ClientSession() as session, session.get(raw_file_url) as response:
            if response.status != 200:
                logger.error(f"Error fetching {raw_file_url}: {response.status}")
                return False

            try:
                content = await response.text()
            except Exception as e:
                logger.error(f"Error reading content from {raw_file_url}: {e}")
                return False

            return bool(re.search(pattern, content))
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching {raw_file_url}: {e}")
        return False


async def find_matched_gists_for_user(username: str, pattern: str) -> list[str]:
    """
    Finds all gists for a given user that contain at least one file matching a given pattern.

    Args:
        username (str): The GitHub username to search for gists.
        pattern (str): The pattern to search for in the files of each gist.

    Returns:
        A list of URLs for all gists that contain at least one file matching the given pattern.
    """
    gists = gists_for_user(username)

    gist_matches = []
    for gist in gists:
        tasks = []
        try:
            async with asyncio.TaskGroup() as tg:
                for file_obj in gist["files"].values():
                    raw_file_url = file_obj["raw_url"]
                    tasks.append(tg.create_task(fetch_and_match(raw_file_url, pattern)))
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
        result["matches"] = await find_matched_gists_for_user(username, pattern)
    except Exception as e:
        result["status"] = str(e)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9876)
