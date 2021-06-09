'''
Functions that support the user menus for both Adminstrators and registered
users are in this class.
'''

from flask import (
    Blueprint, render_template, request
)
import numpy
import pandas as pd
import matplotlib as plt
import networkx as nx
plt.use('agg')

import sqlite3 as sql

from flask import  g

from .auth import login_required
import matplotlib.pyplot as plt
from .db import get_db
####

bp = Blueprint('test_user_index', __name__)
def getReport(thisUser):
    con = get_db()
    main = pd.read_sql_query("SELECT distinct name, u.username, L.rate from UserLocation join Users U on UserLocation.username = U.username join Location L on UserLocation.location_id = L.location_id where entryTime >= (select entryTime from UserLocation where username in (select username from Users where isInfected = 1));", con)
    infectedUser = pd.read_sql_query( "select distinct username from Users where isInfected = 1", con)
    locations = pd.read_sql_query("SELECT name, rate from location", con);
    infectedUserFlatten = infectedUser.values.flatten()
    print(main)
    conn = sql.connect(':memory:')
    plt.clf()
    G = nx.from_pandas_edgelist(main, 'username', 'name', edge_attr='rate')
    if G.has_node(thisUser) is False:
        info = 0
        return(info)
    else:
        path = nx.shortest_path(G, source=infectedUserFlatten[0], target=thisUser)
        shortestPath = {"Locations": path}
        pathFrame = pd.DataFrame(data=shortestPath)
        pathFrame.to_sql('pathFrame', conn, index=False)
        locations.to_sql("location", conn, index=False)
        qry = 'select * from location where name in (select * from pathFrame)'
        result = pd.read_sql_query(qry, conn)
        realRate = result['rate']
        arr = realRate.values.flatten()
        percentage = numpy.prod(arr)
        pos = nx.spring_layout(G)
        #nx.draw(G,pos, with_labels=True, font_weight='bold')
        options = {"node_size": 1000, "alpha": 0.9}
        #nx.draw(G, pos, font_size=6, with_labels=True, node_color='#89CFF0',node_shape="p", font_weight='bold')
        path_edges = list(zip(path, path[1:]))
        labels = {k: k for k in path}
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='#89CFF0',node_shape="o", **options)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='#89CFF0',node_shape="p",**options)
        nx.draw_networkx_labels(G, pos, labels)
        plt.axis('off')
        plt.savefig('./flaskr/static/graph.png', bbox_inches='tight')
        return(percentage)
def changeRate(thisRate, thislocation):
    con = get_db()
    cur = con.cursor()
    qry = "update Location set rate = ? where name LIKE ?"
    cur.execute(qry, (thisRate,thislocation,))
    cur.execute(
        "update UserLocation set rate = (select rate from Location where location_id = UserLocation.location_id) where exists (select rate from Location where location_id = UserLocation.location_id);")
    con.commit()

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
            return render_template('test_user_index/adminOptions.html')

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
            #dummy code
            dummy = 0

        else:

            db = get_db()
            cur = db.cursor()
            #get data from form
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

            percent = "{:.2f}".format(getReport(this_username))

            #print results
            if(float(percent) > 0):
                return render_template('finalReport/graph.html', message='not Admin', value = percent)
            else:
                return render_template('finalReport/newGraph.html', message='not Admin', value=percent)



@bp.route('/user_index_infect', methods=['GET', 'POST'])
@login_required
def adminPageInfect():

    isAdmin = g.user['isAdmin']

    if request.method == 'GET':

        if isAdmin:

            userList= get_db().execute("SELECT * FROM Users WHERE isAdmin = 0 order by username")
            #locationList = get_db().execute("SELECT * FROM Location order by name")
            return render_template('test_user_index/index.html', userList=userList)

    elif request.method == 'POST':

        #get username from form
        infectedUser = request.form['user']

        #execute change
        changeInfectedUser(infectedUser)

        return render_template('finalReport/changesSaved.html', message='Admin')



@bp.route('/user_index_change_prob', methods=['GET', 'POST'])
@login_required
def adminLocProb():

    isAdmin = g.user['isAdmin']

    if request.method == 'GET':

        if isAdmin:
            locationList = get_db().execute("SELECT * FROM Location order by name")

            #generate list of percents
            percents = []
            start = 0
            for x in range(0, 101):
                percents.append(start)
                start = start + 1


            return render_template('test_user_index/change_loc_prob.html', locationList=locationList, percents=percents)

    elif request.method == 'POST':

        #get data from form
        changeLocation = request.form['location'] +"%"
        percent_probability = request.form['prob']
        infect_probablity = float(percent_probability) * 0.01

        #code to change probablity
        changeRate(infect_probablity, changeLocation)

        return render_template('finalReport/changesSaved.html', message='Admin', location = changeLocation, percent = percent_probability)

