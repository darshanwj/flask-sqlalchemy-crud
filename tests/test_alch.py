"""Tests."""
import pytest
from alch import create_app


@pytest.fixture(scope='module')
def app():
    """Setup test app."""
    app = create_app(
        {
            'TESTING': True,
            'MYSQL': 'mysql+mysqldb://root:root@mysql/myalch_test'
        }
    )

    # clear the test db
    from alch.db import Session, Base
    for table in reversed(Base.metadata.sorted_tables):
        Session.execute('TRUNCATE TABLE {}'.format(table))
    Session.commit()

    return app


@pytest.fixture(scope='module')
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_create_user(client):
    """Test creating a user"""
    res = client.post(
        '/user',
        json={
            'name': 'first test user'
        }
    )
    body = res.get_json()
    assert body is not None
    assert 'user' in body
    user = body['user']
    assert 'id' in user and user['id'] == 1
    assert 'name' in user and user['name'] == 'first test user'


def test_update_user(client):
    """Test updating a user"""
    res = client.put(
        '/user/{}'.format(1),
        json={
            'name': 'updated name'
        }
    )
    body = res.get_json()
    assert body is not None
    assert 'user' in body
    user = body['user']
    assert 'id' in user and user['id'] == 1
    assert 'name' in user and user['name'] == 'updated name'


def test_get_user(client):
    res = client.get('/user/{}'.format(1))
    body = res.get_json()
    assert body is not None
    assert 'user' in body
    user = body['user']
    assert 'id' in user and user['id'] == 1
    assert 'name' in user and user['name'] == 'updated name'


def test_home(client):
    """Test home page."""
    assert client.get("/").status_code == 200
