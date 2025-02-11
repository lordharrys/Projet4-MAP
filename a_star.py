import heapq
import math

def a_star(V, adj, s, t):
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(s, t), 0, s)) 
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
        
        # Explore neighbors
        # for neighbor in get_neighbors(current, grid):
        #     tentative_g_score = g + 1  # Assuming each step has a cost of 1
        #     if tentative_g_score < g_score.get(neighbor, float('inf')):
        #         came_from[neighbor] = current
        #         g_score[neighbor] = tentative_g_score
        #         f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
        #         heapq.heappush(open_list, (f_score[neighbor], tentative_g_score, neighbor))
        
    
    return math.inf  # If no path found


def heuristic(a, b):
    
    return

