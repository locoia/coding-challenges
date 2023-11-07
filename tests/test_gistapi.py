"""
This test suite verifies the behavior of the 'gistapi' endpoints under
various scenarios.

No real HTTP requests are made as all external interactions are mocked.
These tests ensure that:

- The service is alive when the '/ping' endpoint is hit.
- Appropriate HTTP 400 errors are returned when 'username' or 'pattern'
  fields are empty.
- Malformed JSON in requests is handled correctly and results in HTTP
  400 errors.
- Valid search requests return HTTP 200 and the correct results.
- Searches resulting in no matches are handled properly with an HTTP
  200 and an empty match list.
- Exceptions caused by invalid GitHub user searches are caught and
  result in HTTP 500 errors.

The use of mocking ensures that tests run in isolation without real-world
side effects, enabling reliable and consistent test results.
"""

import aiohttp
from unittest.mock import AsyncMock, patch


def test_ping(client):
    """
    Ensure the '/ping' route returns a 200 status, indicating the
    service is alive.
    """
    response = client.get("/ping")
    assert response.status_code == 200


def test_search_empty_username(client, post_data):
    """
    Test that submitting an empty 'username' field results in a 400 error.
    Also, validate that the error message returned is as expected.
    """
    post_data["username"] = ""
    response = client.post("/api/v1/search", json=post_data)
    assert response.status_code == 400
    errors = response.get_json()["message"]
    assert any(
        "Username cannot be empty or just whitespace" in error["msg"]
        for error in errors
    )


def test_search_empty_pattern(client, post_data):
    """
    Similar to 'test_search_empty_username', but checks for an
    empty 'pattern' field.
    Also, validate that the error message returned is as expected.
    """
    post_data["pattern"] = ""
    response = client.post("/api/v1/search", json=post_data)
    assert response.status_code == 400
    errors = response.get_json()["message"]
    assert any(
        "Pattern cannot be empty or just whitespace" in error["msg"] for error in errors
    )


def test_search_invalid_json(client):
    """
    Verify that malformed JSON results in a 400 status and the response
    is HTML error page.
    Checking that the HTML error page contains the correct status and title.
    """
    response = client.post(
        "/api/v1/search", data="{bad json:", content_type="application/json"
    )
    assert response.status_code == 400
    data = response.data.decode("utf-8")
    assert "<!doctype html>" in data and "<title>400 Bad Request</title>" in data


def test_successful_search(client, post_data, gist_match_url):
    """
    Confirm that a valid search returns a 200 status and the
    correct match.
    Verifying the search result matches the expected data structure
    and content.
    """
    with patch("gistapi.gistapi.fetch_gists", return_value=[gist_match_url]):
        response = client.post("/api/v1/search", json=post_data)
        assert response.status_code == 200
        assert response.get_json() == {
            "matches": [gist_match_url],
            "pattern": post_data["pattern"],
            "status": "success",
            "username": post_data["username"],
        }


def test_search_pattern_not_found(client, post_data):
    """
    Check that a search with no matches still succeeds with a 200 status
    but empty matches list.
    Ensuring the 'matches' key in the response is an empty list when no
    gists match.
    """
    with patch("gistapi.gistapi.fetch_gists", return_value=[]):
        response = client.post("/api/v1/search", json=post_data)
        assert response.status_code == 200
        assert response.get_json()["matches"] == []


def test_search_with_invalid_user(client, post_data):
    """
    Simulate an exception raised due to an invalid GitHub user and ensure
    proper handling.
    Creating a generic ClientError and manually adding a status attribute
    to mimic error response.
    """
    error_message = "HTTP Error: 404 for URL"
    client_error = aiohttp.ClientError(error_message)

    with patch(
        "gistapi.gistapi.fetch_gists",
        side_effect=AsyncMock(side_effect=client_error),
    ):
        response = client.post("/api/v1/search", json=post_data)
        assert response.status_code == 500
        json_response = response.get_json()
        assert error_message in json_response["message"]
        assert "status" in json_response and json_response["status"] == "error"
