import sqlite3 as sql
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import TextBox
###############
def getPercetage(thisUser):
    G = nx.Graph()
    con = sql.connect("../instance/flaskr.sqlite")
    main = pd.read_sql_query("SELECT name, u.firstName, L.rate from UserLocation join Users U on UserLocation.username = U.username join Location L on UserLocation.location_id = L.location_id where entryTime >= (select entryTime from UserLocation where username in (select username from Users where isInfected = TRUE));", con)
    infectedUser = pd.read_sql_query( "select firstName from Users where isInfected = TRUE", con)
    locations = pd.read_sql_query("SELECT name, rate from location", con);
    infectedUserFlatten = infectedUser.values.flatten()
    conn = sql.connect(':memory:')
    G = nx.from_pandas_edgelist(main, 'firstName', 'name', edge_attr='rate')
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
    #nx.draw(G, with_labels=True, font_weight='bold')
    pos = nx.spring_layout(G)
    options = {"node_size": 500, "alpha": 0.8}
    nx.draw(G, pos, with_labels=True, node_color='#89CFF0',node_shape="p")
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='#fa4a37', **options)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='#fa4a37', width=10, **options)
    plt.axis('equal')
    pretty = "Your rate of infection is: {d}%".format(d =percentage * 100)
    plt.text(0.02, 0.02, pretty, fontsize=14, transform=plt.gcf().transFigure)
    #report png static directory
    plt.show()

def changeInfectedUser(thisUser):
    con = sql.connect("../instance/flaskr.sqlite")
    cur = con.cursor()
    cur.execute("update users set isInfected = 0 where 1=1")
    qry = "update users set isInfected = true where ? = username"
    cur.execute(qry,(thisUser,) )
    con.commit()

def addLocation(name, rate):
    con = sql.connect("../instance/flaskr.sqlite")
    cur = con.cursor()
    qry = "insert into location (name, rate) values(?, ?)"
    cur.execute(qry, (name,rate))
    con.commit()
getPercetage("Lilas")














