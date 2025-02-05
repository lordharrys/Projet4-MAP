import pandas as pd
import math
import networkx as nx
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def distance(lat1, lat2, lon1, lon2):
   
    R = 6378137.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    distance = R * math.acos(math.sin(lat1_rad) * math.sin(lat2_rad) +
                             math.cos(lat1_rad) * math.cos(lat2_rad) * math.cos(lon2_rad - lon1_rad))
    return distance

lat1, lon1 = 51.5074, -0.1278  # Londres
lat2, lon2 = 40.7128, -74.0060  # New York

result = distance(lat1, lat2, lon1, lon2)
print(result)


"""
Processing data and converting it into a Networkx graph.

"""
airports = pd.read_csv("files/airports.csv")
routes = pd.read_csv("files/pre_existing_routes.csv")

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


def plot_network(G):
    """
    Plots the network on a sphere representing the Earth by using cartopy.

    Input:
        - G: a networkx graph representing the network.
    
    """
    fig = plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.Orthographic(central_longitude=0, central_latitude=0))
    ax.set_global()

    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    for node in G.nodes():
        lat, lon = G.nodes[node]["latitude"], G.nodes[node]["longitude"]
        ax.scatter(lon, lat, color='red', s=10, transform=ccrs.PlateCarree())

    for start, end in G.edges():
        lat1, lon1 = G.nodes[start]["latitude"], G.nodes[start]["longitude"]
        lat2, lon2 = G.nodes[end]["latitude"], G.nodes[end]["longitude"]

        ax.plot([lon1, lon2], [lat1, lat2], color='blue', linewidth=0.3, transform=ccrs.PlateCarree())

    plt.title("Réseau aérien mondial avec Cartopy")
    plt.show()

plot_network(G)