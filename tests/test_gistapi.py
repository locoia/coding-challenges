# Created by elvinmirzazada at 23:20 17/02/2023 using PyCharm
import pytest
from gistapi import app

@pytest.fixture
def client():
    with app.app_context():
        with app.test_client() as client:
            yield client


def test_endpoint_available(client):
    response = client.get('/ping')
    assert response.text == 'pong'


def test_pattern_search(client):
    payload = {
        "username": "elvinmirzazada",
        "pattern": "400",
    }
    response = client.post('/api/v1/search', json=payload)
    assert response.status_code == 200 and 'success' == response.json['status']
