import requests


def gists_for_user(username: str, page: int = 1, per_page: int = 30):
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
    gists_url = f"https://api.github.com/users/{username}/gists?{page}&{per_page}"
    response = requests.get(gists_url)
    return response.json()
