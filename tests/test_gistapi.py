import json
import pytest
from constants import constants
from http import HTTPStatus
from gistapi import gistapi

USERNAME = "justdionysus"
VALID_PATTERN = "import requests"
WRONG_PATTERN = "imort requets"
INVALID_PATTERN = "(das../"

@pytest.fixture
def app():
    gistapi.app.config.update({'TESTING': True})
    yield gistapi.app

@pytest.fixture
def client(app):
    return gistapi.app.test_client()


def test_search_success(client):
    response = client.post('/api/v1/search', data=json.dumps({"username": USERNAME, "pattern": VALID_PATTERN}),
        content_type='application/json')
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == constants.STATUS_SUCCESS
    assert len(response.json['matches']) == 1


def test_search_no_username(client):
    response = client.post('/api/v1/search', data=json.dumps({"username": "", "pattern": VALID_PATTERN}),
        content_type='application/json')
    assert response.status_code == HTTPStatus.OK
    assert response.json['error'] == constants.ERROR_NO_USERNAME
    assert response.json['status'] == constants.STATUS_ERROR


def test_search_no_pattern(client):
    response = client.post('/api/v1/search', data=json.dumps({"username": USERNAME, "pattern": ""}),
        content_type='application/json')
    assert response.status_code == HTTPStatus.OK
    assert response.json['error'] == constants.ERROR_NO_PATTERN
    assert response.json['status'] == constants.STATUS_ERROR


def test_search_invalid_pattern(client):
    response = client.post('/api/v1/search', data=json.dumps({"username": USERNAME, "pattern": INVALID_PATTERN}),
        content_type='application/json')
    assert response.status_code == HTTPStatus.OK
    assert response.json['error'] == constants.ERROR_INVALID_PATTERN
    assert response.json['status'] == constants.STATUS_ERROR


def test_search_invalid_pattern(client):
    response = client.post('/api/v1/search', data=json.dumps({"username": USERNAME, "pattern": INVALID_PATTERN}),
        content_type='application/json')
    assert response.status_code == HTTPStatus.OK
    assert response.json['error'] == constants.ERROR_INVALID_PATTERN
    assert response.json['status'] == constants.STATUS_ERROR



