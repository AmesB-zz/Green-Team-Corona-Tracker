'''
init page from flask tutorial
https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/
© Copyright 2010 Pallets
'''

import os

from flask import Flask, render_template

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, '../instance/flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # route for the main home/login page

    @app.route('/')
    def hello():
        '''
        return 'Hello, World!'
        '''
        return render_template('auth/home.html')

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)


    # adding test index.  will land here hopefully after successful login
    from . import test_user_index
    app.register_blueprint(test_user_index.bp)
    app.add_url_rule('/', endpoint='index')

    return app