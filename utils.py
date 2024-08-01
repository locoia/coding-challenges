import re

import requests


def gists_for_user(username: str):
    """Provides the list of gist metadata for a given user, handling pagination.

    This abstracts the /users/:username/gists endpoint from the Github API.
    See https://developer.github.com/v3/gists/#list-a-users-gists for
    more information.

    Args:
        username (string): the user to query gists for

    Returns:
        A list of all gists for the given user.
    """
    gists_url = f"https://api.github.com/users/{username}/gists"
    headers = {"Accept": "application/vnd.github.v3+json"}
    gists = []

    while gists_url:
        response = requests.get(gists_url, headers=headers)
        if response.status_code != 200:
            break
        gists.extend(response.json())
        gists_url = None

        if "Link" in response.headers:
            links = response.headers["Link"].split(",")
            for link in links:
                if 'rel="next"' in link:
                    gists_url = link[link.find("<") + 1 : link.find(">")]
                    break

    return gists


def gist_content(gist_url: str):
    """Fetches the content of a gist by its URL.

    Args:
        gist_url (string): the URL of the gist to fetch content for

    Returns:
        The dict parsed from the json response from the GitHub API containing the gist details.
    """
    response = requests.get(gist_url)
    if response.status_code != 200:
        return None

    return response.json()


def is_pattern_present(raw_url: str, pattern: str):
    """Fetches the content of a file in a gist and checks for a pattern.

    Args:
        raw_url (string): the raw URL of the file
        pattern (string): the pattern to search for

    Returns:
        True if the pattern is found in the file, otherwise False.
    """
    response = requests.get(raw_url, stream=True)
    if response.status_code == 200:
        # Compile the pattern for better performance in loop
        pattern_compiled = re.compile(pattern)

        for chunk in response.iter_content(chunk_size=1024):
            if pattern_compiled.search(chunk.decode("utf-8")):
                return True
    return False
