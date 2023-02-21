import pytest
from requests import HTTPError

from gistapi.exceptions import UserNotFound, GistNotExists


def test_healthcheck(client):
    response = client.get('/ping')
    assert response.text == 'pong'


def test_success_search(client, _mock_get_matched_gists):
    gists = [{"fake_gist": 1}, {"fake_gist": 2}]
    _mock_get_matched_gists.return_value = gists

    payload = {"username": "test", "pattern": "test"}
    response = client.post('/api/v1/search', json=payload)
    assert response.json["status"] == "success"
    assert response.json["matches"] == gists


def test_removed_gist_during_search(client, _mock_get_gist):
    _mock_get_gist.side_effect = GistNotExists

    payload = {"username": "test", "pattern": "test"}
    response = client.post('/api/v1/search', json=payload)
    assert response.json["status"] == "success"


@pytest.mark.parametrize(
    'payload', (
            {"username": "", "pattern": ".*"},
            {"username": "test", "pattern": ""},
            {"username": "", "pattern": ""},
    )
)
def test_search_invalid_payload(client, payload):
    response = client.post('/api/v1/search', json=payload)
    assert response.json["status"] == "failed"


def test_invalid_user(client, _mock_get_user_gists):
    _mock_get_user_gists.side_effect = UserNotFound

    payload = {"username": "test", "pattern": "test"}
    response = client.post('/api/v1/search', json=payload)
    assert response.json["status"] == "failed"


def test_get_user_gists_gh_http_error(client, _mock_get_user_gists):
    _mock_get_user_gists.side_effect = HTTPError

    payload = {"username": "test", "pattern": "test"}
    response = client.post('/api/v1/search', json=payload)
    assert response.json["status"] == "failed"


def test_get_gist_gh_http_error(client, _mock_get_user_gists, _mock_get_gist):
    _mock_get_user_gists.return_value = [1, 2]
    _mock_get_gist.side_effect = HTTPError

    payload = {"username": "test", "pattern": "test"}
    response = client.post('/api/v1/search', json=payload)
    assert response.json["status"] == "failed"
