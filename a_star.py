import heapq
import math
from distance import distance
from directed_edge import directed_edge

def a_star(V, adj, s, t, latitudes, longitudes):
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(s, t, latitudes,longitudes), 0, s)) 
    came_from = {}
    g_score = {s: 0}
    f_score = {s: heuristic(s, t, latitudes, longitudes)}
    
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
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, t, latitudes, longitudes)
                heapq.heappush(open_list, (f_score[neighbor], g_score[neighbor], neighbor))  
        
    
    return math.inf  # If no path found


def heuristic(a, b, latitudes, longitudes):
    dist = distance(latitudes[a], latitudes[b], longitudes[a], longitudes[b])
    return dist

