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
    gists_url = 'https://api.github.com/users/{username}/gists'.format(username=username)
    response = requests.get(gists_url)
    if response.status_code != 200:
        return None

    return response.json()


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
