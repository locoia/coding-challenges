import re
from typing import List

from gistapi.exceptions import GistNotExists, InvalidPayload
from gistapi.services.git_hub_client import GitHubClient


def get_matched_gists(username: str, pattern: str) -> List[dict]:
    if not username or not pattern:
        raise InvalidPayload("Passed username or pattern missed or invalid")

    pattern_obj = re.compile(pattern)

    user_gists = GitHubClient.get_user_gists(username)

    matches = []
    for gist in user_gists:
        try:
            GitHubClient.get_gist(gist)
        except GistNotExists:
            continue

        for f in gist.content:
            if pattern_obj.search(f):
                matches.append(gist.data)
                break
    return matches
