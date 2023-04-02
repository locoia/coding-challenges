"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""
import re
from typing import Pattern

import requests


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
    response = requests.get(gists_url)
    return response.json()


def is_matching_gist(gist: dict, regex_pattern: Pattern) -> bool:
    """
    - uses the raw_url to get larger than > 1 mb files
    More info about the Endpoints: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28
    """
    if (files := gist.get('files')) is not None:
        for file in files:
            if (raw_url := gist['files'][file].get('raw_url')) is not None:
                # TODO this .get should be done async
                response = requests.get(raw_url)
                response.raise_for_status()
                if response.status_code == 200 and \
                        re.search(regex_pattern, response.text):
                    return True
    return False
