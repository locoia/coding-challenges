from unittest.mock import AsyncMock, patch

import pytest
import responses

from gistapi.gistapi import find_matching_gists


# Attribution: https://stackoverflow.com/a/59351425
class MockResponse:
    def __init__(self, text, status, reason=""):
        self._text = text
        self.status = status
        self.reason = reason

    async def text(self):
        return self._text

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


def test_ping(client):
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.text == "pong"


@responses.activate
def test_search_error_fetching_gists_for_user(client):
    gists_for_user_url = "https://api.github.com/users/test/gists"
    responses.get(gists_for_user_url, status=404)
    username = "test"
    pattern = "test_pattern"
    response = client.post("/api/v1/search", json={"username": username, "pattern": pattern})

    assert response.status_code == 404
    assert response.json == {
        "status": f"404 Client Error: Not Found for url: {gists_for_user_url}",
        "username": username,
        "pattern": pattern,
        "matches": [],
    }


@responses.activate
def test_search_error_finding_matching_gists(client, faker):
    gists_for_user_url = "https://api.github.com/users/test/gists"
    responses.get(gists_for_user_url, json=[{"files": {"test_file": {"raw_url": faker.url()}}}])
    username = "test"
    pattern = "test_pattern"
    with patch(
        "gistapi.gistapi.find_matching_gists", side_effect=AsyncMock(side_effect=Exception("Critical error"))
    ):
        response = client.post("/api/v1/search", json={"username": username, "pattern": pattern})

    assert response.status_code == 500
    assert response.json == {
        "status": "Critical error",
        "username": username,
        "pattern": pattern,
        "matches": [],
    }


@responses.activate
def test_search_success(client, faker):
    gists_for_user_url = "https://api.github.com/users/test/gists"
    responses.get(gists_for_user_url, json=[{"files": {"test_file": {"raw_url": faker.url()}}}])
    username = "test"
    pattern = "test_pattern"
    matched_gist_url = faker.url()
    with patch("gistapi.gistapi.find_matching_gists", return_value=[matched_gist_url]):
        response = client.post("/api/v1/search", json={"username": username, "pattern": pattern})

    assert response.status_code == 200
    assert response.json == {
        "status": "success",
        "username": username,
        "pattern": pattern,
        "matches": [matched_gist_url],
    }


@pytest.mark.asyncio
async def test_find_matching_gists_success(faker):
    matched_gist_url = faker.url()
    unmatched_gist_url = faker.url()
    gists = [
        {
            "files": {
                "test_file": {
                    "raw_url": faker.url(),
                }
            },
            "html_url": matched_gist_url,
        },
        {
            "files": {
                "test_file": {
                    "raw_url": faker.url(),
                }
            },
            "html_url": unmatched_gist_url,
        },
    ]
    pattern = "test_pattern"
    matched_response = MockResponse(pattern, 200)
    unmatched_response = MockResponse("unmatched", 200)
    with patch(
        "gistapi.gistapi.aiohttp.ClientSession.get", side_effect=[matched_response, unmatched_response]
    ):
        result = await find_matching_gists(gists, pattern)

    assert result == [matched_gist_url]


@pytest.mark.asyncio
async def test_find_matching_gists_success_with_logged_exceptions(faker):
    matched_gist_url = faker.url()
    gists = [
        {
            "files": {
                "test_file": {
                    "raw_url": faker.url(),
                }
            },
            "html_url": matched_gist_url,
        },
        {
            "files": {
                "test_file": {
                    "raw_url": faker.url(),
                }
            },
            "html_url": faker.url(),
        },
    ]
    pattern = "test_pattern"
    matched_response = MockResponse(pattern, 200)
    failed_response = MockResponse("unmatched", 404, "Not Found")
    with patch("gistapi.gistapi.aiohttp.ClientSession.get", side_effect=[matched_response, failed_response]):
        result = await find_matching_gists(gists, pattern)

    assert result == [matched_gist_url]
