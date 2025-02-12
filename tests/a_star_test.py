# Description: Test cases for A* algorithm
from a_star import a_star
from a_star import heuristic
from distance import distance
from dijsktra_own import directed_edge

# Example graph    
V = [0, 1, 2, 3, 4]
latitudes = [0, 1, 2, 3, 4]
longitudes = [0, 1, 2, 3, 4]
adj = {
    0: [directed_edge(0, 1, heuristic(0,1,latitudes,longitudes)), directed_edge(0, 2, heuristic(0,2,latitudes,longitudes))],
    1: [directed_edge(1, 3, heuristic(1,3,latitudes,longitudes))],
    2: [directed_edge(2, 1, heuristic(2,1,latitudes,longitudes)), directed_edge(2, 3, heuristic(2,3,latitudes,longitudes))],
    3: [directed_edge(3, 4, heuristic(3,4,latitudes,longitudes))],
    4: []
}


# Test 1: Path from 0 to 4
s, t = 0, 4

path = a_star(V, adj, s, t, latitudes, longitudes)
print(f"Path from {s} to {t}: {path}")  

# Test 2: Path from 0 to 3
s, t = 0, 3
path = a_star(V, adj, s, t, latitudes, longitudes)
print(f"Path from {s} to {t}: {path}")  

# Test 3: Path from 2 to 4
s, t = 2, 4
path = a_star(V, adj, s, t, latitudes, longitudes)
print(f"Path from {s} to {t}: {path}") 