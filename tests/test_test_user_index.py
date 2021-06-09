import pytest
from flask import g, session
from flaskr.db import get_db
from flaskr.test_user_index import getReport

def test_get_report(app):
	with app.app_context():
		assert getReport("eringwood0") == 0