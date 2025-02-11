import heapq
import math
from distance import distance
def a_star(V, adj, s, t, latitudes, longitudes):
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(s, t, latitudes,longitudes), 0, s)) 
    came_from = {}
    g_score = {s: 0}
    f_score = {s: heuristic(s, t)}
    
    while open_list:
        _, g, current = heapq.heappop(open_list)
        
        # If we've reached the goal
        if current == t:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(s)
            return path[::-1]  # Reverse the path
        
        

        for edge in adj[current]:
            neighbor = edge.w
            tentative_g_score = g_score[current] + edge.weight

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:  
                came_from[neighbor] = current  
                g_score[neighbor] = tentative_g_score  
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, t)
                heapq.heappush(open_list, (f_score[neighbor], g_score[neighbor], neighbor))  
        
    
    return math.inf  # If no path found


def heuristic(a, b, latitudes, longitudes):
    dist = distance(latitudes[a], latitudes[b], longitudes[a], longitudes[b])
    return dist

# Example graph    
V = [0, 1, 2, 3, 4]
adj = {
    0: [directed_edge(0, 1, 4), directed_edge(0, 2, 1)],
    1: [directed_edge(1, 3, 1)],
    2: [directed_edge(2, 1, 2), directed_edge(2, 3, 5)],
    3: [directed_edge(3, 4, 3)],
    4: []
}

latitudes = [0, 1, 2, 3, 4]
longitudes = [0, 1, 2, 3, 4]

# Test 1: Path from 0 to 4
s, t = 0, 4

path = a_star(V, adj, s, t, latitudes, longitudes)
print(f"Path from {s} to {t}: {path}")  # Expected: [0, 2, 1, 3, 4]

# Test 2: Path from 0 to 3
s, t = 0, 3
path = a_star(V, adj, s, t, latitudes, longitudes)
print(f"Path from {s} to {t}: {path}")  # Expected: [0, 2, 1, 3]

# Test 3: Path from 2 to 4
s, t = 2, 4
path = a_star(V, adj, s, t, latitudes, longitudes)
print(f"Path from {s} to {t}: {path}")  # Expected: [2, 1, 3, 4]
