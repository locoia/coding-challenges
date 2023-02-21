import pytest

from main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def _mock_get_matched_gists(mocker):
    return mocker.patch("gistapi.api.gists.get_matched_gists")


@pytest.fixture
def _mock_get_user_gists(mocker):
    return mocker.patch("gistapi.utils.gist_utils.GitHubClient.get_user_gists")


@pytest.fixture
def _mock_get_gist(mocker):
    return mocker.patch("gistapi.utils.gist_utils.GitHubClient.get_gist")
