import re

import pytest
from unittest.mock import patch, MagicMock

from gistapi import is_matching_gist

gists = {
    'files': {
        'file_1': {'raw_url': 'fancy_url'}
    }
}
pattern = re.compile(r'\d\d')
# TODO This could be done via this https://pypi.org/project/requests-mock/ as well
response_mock = MagicMock()
response_mock.status_code = 200
response_mock.text = '213213'
request_mock = MagicMock()
request_mock.get.return_value = response_mock


@pytest.mark.skip(reason="Not implemented")
def test_search_endpoint_simple_flow():
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented")
def test_search_endpoint_with_invalid_regex():
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented")
def test_gists_for_user():
    raise NotImplementedError


def test_is_matching_gist_empy_gist():
    assert is_matching_gist({}, pattern) is False


@patch('gistapi.gistapi.requests', request_mock)
def test_is_matching_gist_valid_gist():
    assert is_matching_gist(gists, pattern) is True
