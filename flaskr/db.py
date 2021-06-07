
'''
database config file from flask tutorial
https://flask.palletsprojects.com/en/2.0.x/tutorial/database/
© Copyright 2010 Pallets\
Modified for EOU CS362 Corona Virus project
'''


import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


        #testing how to initialize

        db.execute(
            'INSERT INTO Users (username, passwordHash,firstName, lastName, isInfected, isAdmin) VALUES (?, ?, ?, ?, ?, ?)',
            ('Admin', generate_password_hash('test'), 'Dan', 'Lea', False, True)
        )
        db.commit()

        populate_test()



@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def populate_test():
    con = get_db()
    cur = con.cursor()
    userLocations = open("./DB/populateUserLocation")
    locations = open("./DB/populateLocation")
    users = open("./DB/populateUsers")
    userLocationsSql = userLocations.read()
    locationsSql = locations.read()
    usersSql = users.read()
    cur.executescript(userLocationsSql)
    cur.executescript(usersSql)
    cur.executescript(locationsSql)
    cur.execute(
        "update UserLocation set rate = (select rate from Location where location_id = UserLocation.location_id) where exists (select rate from Location where location_id = UserLocation.location_id);")
    cur.execute(
        "update UserLocation set username = (select u.username from Users u where UserLocation.username = u.ROWID);")
    con.commit()