from .db import get_db
import sqlite3 as sql
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
###############


def getReport(thisUser):
    G = nx.Graph()
    con = get_db()
    main = pd.read_sql_query("SELECT name, u.username, L.rate from UserLocation join Users U on UserLocation.username = U.username join Location L on UserLocation.location_id = L.location_id where entryTime >= (select entryTime from UserLocation where username in (select username from Users where isInfected = TRUE));", con)
    infectedUser = pd.read_sql_query( "select username from Users where isInfected = TRUE", con)
    locations = pd.read_sql_query("SELECT name, rate from location", con);
    infectedUserFlatten = infectedUser.values.flatten()
    conn = sql.connect(':memory:')
    G = nx.from_pandas_edgelist(main, 'username', 'name', edge_attr='rate')
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

    options = {"node_size": 500, "alpha": 0.9}
    #nx.draw(G, pos, font_size=6, with_labels=True, node_color='#89CFF0',node_shape="p", font_weight='bold')
    path_edges = list(zip(path, path[1:]))
    labels = {k: k for k in path}
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='#89CFF0',node_shape="p", **options)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='#89CFF0',node_shape="p", width=10, **options)
    nx.draw_networkx_labels(G, pos, labels)
    plt.axis('equal')
    pretty = "Your rate of infection is: {d}%".format(d =percentage * 100)
    plt.text(0.02, 0.02, pretty, fontsize=14, transform=plt.gcf().transFigure)
    #report png static directory
    plt.show()


def addLocation(name, rate):
    con = get_db()
    cur = con.cursor()
    qry = "insert into location (name, rate) values(?, ?)"
    cur.execute(qry, (name,rate))
    con.commit()

# def populate():
#     #con = sql.connect("../instance/flaskr.sqlite")
#     con = get_db()
#     cur = con.cursor()
#     userLocations = open("../DB/populateUserLocation")
#     locations = open("../DB/populateLocation")
#     users = open("../DB/populateUsers")
#     userLocationsSql = userLocations.read()
#     locationsSql = locations.read()
#     usersSql = users.read()
#     cur.executescript(userLocationsSql)
#     cur.executescript(usersSql)
#     cur.executescript(locationsSql)
#     cur.execute("update UserLocation set rate = (select rate from Location where location_id = UserLocation.location_id) where exists (select rate from Location where location_id = UserLocation.location_id);")
#     cur.execute("update UserLocation set username = (select u.username from Users u where UserLocation.username = u.ROWID);")
#     con.commit()

