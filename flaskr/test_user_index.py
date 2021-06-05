from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import functools

from werkzeug.exceptions import abort
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

from .auth import login_required
from .db import get_db

bp = Blueprint('test_user_index', __name__)



@bp.route('/user_index', methods=['GET', 'POST'])
@login_required
def tux():

    userList= get_db().execute("SELECT * FROM Users order by username")

    return render_template('test_user_index/index.html', userList=userList)
