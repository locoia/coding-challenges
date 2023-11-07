"""
This module provides pytest fixtures for the gistapi application.
"""
import pytest
from gistapi.gistapi import app


@pytest.fixture
def client():
    """
    Set up a test client for the application.

    This client will be used in test functions to make requests to the app
    and provides a client instance to test functions.
    """
    with app.app_context():
        with app.test_client() as client:
            yield client


@pytest.fixture
def post_data():
    """
    Provides a default payload for search API post requests.

    This is a common payload structure used across multiple tests.
    """
    return {"username": "justdionysus", "pattern": "import requests"}


@pytest.fixture
def gist_match_url():
    """
    A mock URL representing a gist that matches the search pattern.

    This URL is used to simulate a search result in tests.
    """
    return "https://api.github.com/gists/65e6162d99c2e2ea8049b0584dd00912"
