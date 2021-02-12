""" Tests """
import pytest
from alch import create_app


@pytest.fixture
def app():
    """ Setup test app """
    app = create_app(
        {
            'TESTING': True,
            'MYSQL': 'mysql+mysqldb://root:root@mysql/myalch_test'
        }
    )

    yield app

    # clear test db here


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_home(client):
    assert client.get("/").status_code == 200
