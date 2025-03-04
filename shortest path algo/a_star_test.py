# Description: Test cases for A* algorithm
from a_star import a_star
import networkx as nx
from distance import distance

# Create a small graph with 5 airports
G = nx.DiGraph()

# Add nodes (airports)
airports = [
    {"ID": "A1", "name": "Airport 1", "city": "City 1", "country": "Country 1", "latitude": 0, "longitude": 0},
    {"ID": "A2", "name": "Airport 2", "city": "City 2", "country": "Country 2", "latitude": 1, "longitude": 1},
    {"ID": "A3", "name": "Airport 3", "city": "City 3", "country": "Country 3", "latitude": 2, "longitude": 2},
    {"ID": "A4", "name": "Airport 4", "city": "City 4", "country": "Country 4", "latitude": 3, "longitude": 3},
    {"ID": "A5", "name": "Airport 5", "city": "City 5", "country": "Country 5", "latitude": 4, "longitude": 4}
]

for airport in airports:
    G.add_node(airport["ID"], name=airport["name"], city=airport["city"], country=airport["country"], latitude=airport["latitude"], longitude=airport["longitude"])

# Add edges (routes) with distances
routes = [
    {"ID_start": "A1", "ID_end": "A2","weight": 100},
    {"ID_start": "A2", "ID_end": "A3","weight": 200},
    {"ID_start": "A3", "ID_end": "A4",'weight': 300},
    {"ID_start": "A4", "ID_end": "A5","weight": 400},
]

for route in routes:
    start, end = route["ID_start"], route["ID_end"]
    if start in G.nodes and end in G.nodes:
        lat1 = G.nodes[start]["latitude"]
        lon1 = G.nodes[start]["longitude"]
        lat2 = G.nodes[end]["latitude"]
        lon2 = G.nodes[end]["longitude"]
        dist = distance(lat1, lon1, lat2, lon2)
        G.add_edge(start, end, weight=dist)



# Test 1: Path from 0 to 4
s, t = "A1", "A2"

path = a_star(G,s,t)
solution = nx.shortest_path(G, source=s, target=t, weight='weight')
print(f"Path from {s} to {t}: {path}") 
print("real solution :",solution) 


# Test 2: Path from 0 to 3
s, t = "A1", "A3"
path = a_star(G,s,t)
solution = nx.shortest_path(G, source=s, target=t, weight='weight')
print(f"Path from {s} to {t}: {path}") 
print("real solution :", solution) 

# Test 3: Path from 2 to 4
s, t = "A2", "A4"
path = a_star(G,s,t)
solution = nx.shortest_path(G, source=s, target=t, weight='weight')
print(f"Path from {s} to {t}: {path}") 
print("real solution :",solution) 