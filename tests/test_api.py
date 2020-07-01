import pytest
from src import main


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    # create the app with common test config
    app = main.app

    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_index(client):
    response = client.get("/")
    print(response)
    assert b"config-server" in response.data
