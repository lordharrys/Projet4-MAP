import heapq
import math
import networkx as nx
from distance import distance


def a_star(G, s, t):
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(s, t, G), 0, s)) 
    came_from = {}
    g_score = {s: 0}
    f_score = {s: heuristic(s, t, G)}
    
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
        
        for neighbor in G.neighbors(current):
            tentative_g_score = g_score[current] + G[current][neighbor].get('weight', 1)

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:  
                came_from[neighbor] = current  
                g_score[neighbor] = tentative_g_score  
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, t, G)
                heapq.heappush(open_list, (f_score[neighbor], g_score[neighbor], neighbor))  
    
    return math.inf  # If no path found


def heuristic(a, b, G):
    dist = distance(G.nodes[a]["latitude"], G.nodes[b]["latitude"], G.nodes[a]["longitude"], G.nodes[b]["longitude"])
    return dist

