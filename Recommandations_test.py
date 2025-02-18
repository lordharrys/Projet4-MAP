from Recommandations import recommandations
import networkx as nx
from distance import distance

# Create a small graph with 5 airports
G = nx.DiGraph()

# Add nodes (airports)
airports = [
    {"ID": "A1", "name": "Airport 1", "city": "City 1", "country": "Country 1", "latitude": 40.7128, "longitude": -74.0060},
    {"ID": "A2", "name": "Airport 2", "city": "City 2", "country": "Country 2", "latitude": 34.0522, "longitude": -118.2437},
    {"ID": "A3", "name": "Airport 3", "city": "City 3", "country": "Country 3", "latitude": 51.5074, "longitude": -0.1278},
    {"ID": "A4", "name": "Airport 4", "city": "City 4", "country": "Country 4", "latitude": 48.8566, "longitude": 2.3522},
    {"ID": "A5", "name": "Airport 5", "city": "City 5", "country": "Country 5", "latitude": 35.6895, "longitude": 139.6917}
]

for airport in airports:
    G.add_node(airport["ID"], name=airport["name"], city=airport["city"], country=airport["country"], latitude=airport["latitude"], longitude=airport["longitude"])

# Add edges (routes) with distances
routes = [
    {"ID_start": "A1", "ID_end": "A2"},
    {"ID_start": "A2", "ID_end": "A3"},
    {"ID_start": "A3", "ID_end": "A4"},
    {"ID_start": "A4", "ID_end": "A5"},
    {"ID_start": "A5", "ID_end": "A1"}
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

# Define waiting times and prices (dummy values for testing)
waiting_times = {
    "A1": 10,
    "A2": 20,
    "A3": 30,
    "A4": 40,
    "A5": 50
}

prices = {
    ("A1", "A2"): 100,
    ("A2", "A3"): 200,
    ("A3", "A4"): 300,
    ("A4", "A5"): 400,
    ("A5", "A1"): 500
}
J = [("A1", "A2"), ("A2", "A3"), ("A3", "A4"), ("A4", "A5"), ("A5", "A1")]
time = {
    ("A1", "A2"): 1,
    ("A2", "A3"): 1,
    ("A3", "A4"): 1,
    ("A4", "A5"): 1,
    ("A5", "A1"): 1
}

# Test the recommandations function
recommandations(G, waiting_times, prices,J,time)