import os.path
from typing import Union, Generator, Callable

import requests

from gistapi.services.schemas import Gist
from gistapi.exceptions import GistNotExists, UserNotFound

URI = 'https://api.github.com'
GET_GIST = os.path.join(URI, 'gists/{gist_id}')
GET_USER_GISTS = os.path.join(URI, 'users/{user_name}/gists')


class GitHubClient:

    @staticmethod
    def __request(url: str, response_custom_handler: Callable, **request_kwargs):
        response = requests.get(
            url=url,
            **request_kwargs,
        )
        response_custom_handler(response)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_gist(gist: Gist) -> None:
        def handler(r):
            if r.status_code == 404:
                raise GistNotExists

        data = GitHubClient.__request(
            url=GET_GIST.format(gist_id=gist.id),
            response_custom_handler=handler,
            headers={'accept': 'application/vnd.github+json'},
        )
        gist.content = (f["content"] for f in data["files"].values())

    @staticmethod
    def get_user_gists(
            user_name: str,
            params: Union[None, dict] = None,
    ) -> Generator[Gist, None, None]:
        def handler(r):
            if r.status_code == 404:
                raise UserNotFound("Username does not exist")

        data = GitHubClient.__request(
            url=GET_USER_GISTS.format(user_name=user_name),
            response_custom_handler=handler,
            params=params or {},
        )

        return (Gist(g["id"], g) for g in data)
