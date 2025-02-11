# Description: Test cases for A* algorithm
from a_star import a_star
from a_star import heuristic
from distance import distance
from dijsktra_own import directed_edge

# Example graph
V = [0, 1, 2, 3, 4]
adj = {
    0: [directed_edge(0, 1, 4), directed_edge(0, 2, 1)],
    1: [directed_edge(1, 3, 1)],
    2: [directed_edge(2, 1, 2), directed_edge(2, 3, 5)],
    3: [directed_edge(3, 4, 3)],
    4: []
}

# Test 1: Path from 0 to 4
s, t = 0, 4
path = a_star(V, adj, s, t)
print(f"Path from {s} to {t}: {path}")  # Expected: [0, 2, 1, 3, 4]

# Test 2: Path from 0 to 3
s, t = 0, 3
path = a_star(V, adj, s, t)
print(f"Path from {s} to {t}: {path}")  # Expected: [0, 2, 1, 3]

# Test 3: Path from 2 to 4
s, t = 2, 4
path = a_star(V, adj, s, t)
print(f"Path from {s} to {t}: {path}")  # Expected: [2, 1, 3, 4]

# Test 4: No path (disconnected graph)
V = [0, 1, 2]
adj = {
    0: [directed_edge(0, 1, 1)],
    1: [],
    2: []
}
s, t = 0, 2
path = a_star(V, adj, s, t)
print(f"Path from {s} to {t}: {path}")  # Expected: []