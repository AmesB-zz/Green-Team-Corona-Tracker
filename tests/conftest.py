'''
conftest framework modified from flask tutorial
https://flask.palletsprojects.com/en/2.0.x/tutorial/tests/
© Copyright 2010 Pallets
'''

import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app()

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app
    os.close(db_fd)
    os.unlink(db_path)

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def auth(client):
    return AuthActions(client)
