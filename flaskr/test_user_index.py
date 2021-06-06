from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import pandas as pd
import functools

from werkzeug.exceptions import abort
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

from .auth import login_required
from .db import get_db
####


bp = Blueprint('test_user_index', __name__)

def changeInfectedUser(thisUser):
    con = get_db()
    cur = con.cursor()
    cur.execute("update users set isInfected = 0 where 1=1")
    qry = "update users set isInfected = 1 where ? = username"
    cur.execute(qry,(thisUser,) )
    con.commit()

@bp.route('/user_index', methods=['GET', 'POST'])
@login_required
def tux():

    # check if logged in user is an admin
    isAdmin = g.user['isAdmin']

    if request.method == 'GET':


        if isAdmin:
            # go to admin page
            # Disclude the admin????
            userList= get_db().execute("SELECT * FROM Users order by username")

            return render_template('test_user_index/index.html', userList=userList)

        else:

            timeList = ['00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00',
                        '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30',
                        '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                        '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00',
                        '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30',
                        '23:00', '23:30']

            #populate location list
            locationList = get_db().execute("SELECT * FROM Location")


            return render_template('test_user_index/nonAdmin_index.html', timeList=timeList, locationList=locationList)

    elif request.method == 'POST':


        if isAdmin:

            infectedUser = request.form['user']

            # code to change database here
            changeInfectedUser(infectedUser)

            return render_template('finalReport/changesSaved.html', message='Admin')

        else:

            db = get_db()
            cur = db.cursor()
            this_username = g.user['username']
            location = request.form['location']
            time = request.form['time']

            qry = 'SELECT location_id FROM Location WHERE name LIKE "{fname}%"'.format(fname = location)
            location_idf = pd.read_sql_query(qry, db)
            newLocation = location_idf.values.flatten()

            db.execute(
                'INSERT INTO UserLocation (location_id, entryTime, username) VALUES (?, ?, ?)',
                (int(newLocation[0]), str(time), str(this_username))
            )

            cur.execute(
                "update UserLocation set rate = (select rate from Location where location_id = UserLocation.location_id) where exists (select rate from Location where location_id = UserLocation.location_id);")

            db.commit()



            return render_template('finalReport/graph.html', message='not Admin')
