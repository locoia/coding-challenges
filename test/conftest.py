import pytest
from gistapi import create_app


@pytest.fixture(scope="session")
def app_config():
    app_inst = create_app()
    yield app_inst


@pytest.fixture(scope="session")
def app(app_config):
    app = app_config.test_client()
    ctx = app_config.app_context()
    ctx.push()
    yield app
    ctx.pop()
