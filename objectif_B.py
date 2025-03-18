import Projet4 
import data_processing
import distance
import unittest
import networkx as nx
import csv
import pandas as pd
from distance import distance

#à ajouter : modéliser avec SIR

#define a region that contains the airports in a certain perimeter around the starting airport
def define_region(latitude,longitude,perimeter,airports):
    region = []
    for airport in airports:
        if (latitude - perimeter <= airports[airport]["latitude"] <= latitude + perimeter) and (longitude - perimeter <= airports[airport]["longitude"] <= longitude + perimeter):
                region.append(airport)
    return region

#return the degrees of the nodes in the region that are connected to nodes outside the region
def get_region_degrees(G,region):
    degrees = {}
    for node in region:
        degrees[node] = 0
    for node in G.nodes:
        if node in region:
            for neighbor in G.neighbors(node):
                if neighbor not in region:
                    degrees[node] +=1
    return degrees

#remove the npdes with the highest degrees outside the region from the graph
def remove_edges(G,edges,degrees):
    sorted_degrees = dict(sorted(degrees.items(), key=lambda item: item[1]))
    for key in list(sorted_degrees.keys())[-5:]:
        G.remove_node(key)
    return G,edges

#Objectif B when we know where the disease started
def objectif_B_start(G,edges,start,perimeter):
    region_disease = define_region(G.nodes[start]["latitude"],G.nodes[start]["longitude"],perimeter,G.nodes)
    degrees_region_disease = get_region_degrees(G,region_disease)
    G,edges = remove_edges(G,edges,degrees_region_disease)
    return G,edges
 
 
#Objectif B when we don't know where the disease started
def objectif_B(G):
    closeness_centrality = nx.closeness_centrality(G)
    sorted_closeness = dict(sorted(closeness_centrality.items(), key=lambda item: item[1]))

    # Supprimer les 15 aéroports ayant la centralité de proximité la plus faible (les plus proches de tous les autres)
    airports_to_remove = list(sorted_closeness.keys())[:15]
    for airport in airports_to_remove:
        G.remove_node(airport)
    return G

G_small, filtered_routes = data_processing.data_processing("files/airports.csv", "files/pre_existing_routes.csv")

G_new=(objectif_B(G_small))
print(G_new.nodes)



