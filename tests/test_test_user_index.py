import pytest
from flask import g, session
from flaskr.db import get_db
from flaskr.test_user_index import getReport, changeInfectedUser

def test_get_report(app):
	with app.app_context():
		db = get_db()
		assert getReport("eringwood0") == 0
		changeInfectedUser("adooney21")
		assert getReport("eringwood0") > 0
