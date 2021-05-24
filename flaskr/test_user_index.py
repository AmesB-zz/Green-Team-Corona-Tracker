from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('test_user_index', __name__)

@bp.route('/')
def test_user_index():



    return render_template('blog/index.html')