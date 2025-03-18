import Projet4 
import data_processing
import distance
import unittest
import networkx as nx
import csv
import pandas as pd
from distance import distance

"""
The goal of this objectif is to remove the airports that are the disease's home.

parameters:
- G: the graph of airports
- nodes: the nodes that are the disease

returns:
- G: the modified graph with the nodes removed

"""

# define a function that returns strongly connected components of graph G
def strongly_connected_components(G):
    components = list(nx.strongly_connected_components(G))
    return components

# define a function that takes a list of nodes and removes all components that contain these nodes
def remove_components(G, components, nodes):
    for component in components:
        if any(node in component for node in nodes):
            for node in component:
                G.remove_node(node)
    return G

