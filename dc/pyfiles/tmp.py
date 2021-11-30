import numpy as np
import networkx as nx
import json
import matplotlib.pyplot as plt

fconn = open("../modfiles/test.json")
conn = json.load(fconn)

nodes_list = list(conn.keys())

G = nx.Graph()
G.add_nodes_from(nodes_list)

edges_list = []
visited = []

for cell in conn:
    visited.append(cell)
    for neighbor in conn[cell]:
        if neighbor not in visited:
            edges_list.append((cell, neighbor))

G.add_edges_from(edges_list)

nx.draw(G)




