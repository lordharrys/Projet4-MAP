import pandas as pd
import networkx as nx
from distance import distance


def data_preprocessing(airports, routes):
    """
    """
    airports = pd.read_csv(airports)
    routes = pd.read_csv(routes)
    latitudes = [lat for lat in airports["latitude"]]
    longitudes = [lon for lon in airports["longitude"]]

    G = nx.DiGraph()

    for _, row in airports.iterrows():
        G.add_node(row["ID"], name=row["name"], city=row["city"], country=row["country"], 
                latitude=row["latitude"], longitude=row["longitude"])

    for _, row in routes.iterrows():
        start, end = row["ID_start"], row["ID_end"]
        
        if start in G.nodes and end in G.nodes:
            lat1, lon1 = G.nodes[start]["latitude"], G.nodes[start]["longitude"]
            lat2, lon2 = G.nodes[end]["latitude"], G.nodes[end]["longitude"]
            
            dist = distance(lat1, lon1, lat2, lon2)  
            G.add_edge(start, end, weight=dist)
    
    return airports, routes, G, latitudes, longitudes


airports, routes, G, latitudes, longitudes = data_preprocessing("files/airports.csv", "files/pre_existing_routes.csv")