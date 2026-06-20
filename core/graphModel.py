#########################################################
#   Written by  :   Hassan Ayoub                        #
#   Date        :   December 3, 2025                    #
#   Purpose     :   Storing graphs to be                # 
#                   displyed on animation view          #
#########################################################

import math
import networkx as nx
import random

# Graph class
class Graph:

    # Constructor
    def __init__(self):
        # This dictionary will store data of the following format:  
        # nodes['nodeLabel'] = {'xCoordinate' : x, 'yCoordinate' : y}
        self.nodes = {}

        # This is an adjacency list to store graph
        self.adjList = {}

    # Method to add nodes to a graph
    def addNode(self, nodeId, x, y):
        self.nodes[nodeId] = {'x': x, 'y': y}
        self.adjList[nodeId] = []
    
    # Method to add edge to a graph
    def addEdge(self, node1, node2):
        self.adjList[node1].append(node2)
        self.adjList[node2].append(node1)


# Function which returns a Desargues Graph
def getDesarguesGraph(canvasWidth=800, canvasHeight=800):
    g = Graph()

    # Determine the radius, subtract 80 to leave some margin
    radius = (min(canvasWidth, canvasHeight) // 2) - 80
    centerX = canvasWidth // 2
    centerY = canvasHeight // 2

    # The order of vertices
    order = list(range(20))  
    n = len(order)

    for idx, node in enumerate(order):
        # Full rotation is 2pi radians, so each node will get 2pi / n
        # Multiplied by index to actually move around the circle
        angle = (2 * math.pi * idx) / n

        x = centerX + radius * math.cos(angle)
        y = centerY + radius * math.sin(angle)

        g.addNode(str(node), x, y)

    G = nx.generators.small.desargues_graph()
    for n in G.nodes():
        for u in G.adj[n]:
            g.addEdge(str(n), str(u))
    return g

# Function which returns a Karate Club Graph
def getKarateClubGraph(canvasWidth=800, canvasHeight=800):
    g = Graph()

    G = nx.karate_club_graph()
    n = len(G.nodes())

    for node in range(n):
        g.addNode(str(node), random.uniform(50, canvasWidth - 50), random.uniform(50, canvasHeight - 50))

    for n in G.nodes():
        for u in G.adj[n]:
            g.addEdge(str(n), str(u))
    return g

# Function which returns a Icosahedral Graph (planar, 3-connected graphs)
def getIcosahedralGraph(canvasWidth=800, canvasHeight=800):
    g = Graph()

    G = nx.icosahedral_graph()
    n = len(G.nodes())

    for node in range(n):
        g.addNode(str(node), random.uniform(50, canvasWidth - 50), random.uniform(50, canvasHeight - 50))

    for n in G.nodes():
        for u in G.adj[n]:
            g.addEdge(str(n), str(u))
    return g

# Function which returns a Dodecahedral Graph
def getDodecahedralGraph(canvasWidth=800, canvasHeight=800):
    g = Graph()

    G = nx.dodecahedral_graph()
    n = len(G.nodes())

    for node in range(n):
        g.addNode(str(node), random.uniform(50, canvasWidth - 50), random.uniform(50, canvasHeight - 50))

    for n in G.nodes():
        for u in G.adj[n]:
            g.addEdge(str(n), str(u))
    return g

# Function which returns a LES_MISERABLES Graph
def getFlorentineFamiliesGraph(canvasWidth=800, canvasHeight=800):
    g = Graph()

    G = nx.florentine_families_graph()

    integer_map = {name: i for i, name in enumerate(G.nodes())}
    G = nx.relabel_nodes(G, integer_map)

    n = len(G.nodes())

    for node in range(n):
        g.addNode(str(node), random.uniform(50, canvasWidth - 50), random.uniform(50, canvasHeight - 50))

    for n in G.nodes():
        for u in G.adj[n]:
            g.addEdge(str(n), str(u))
    print(len(g.nodes), len(g.adjList))
    return g