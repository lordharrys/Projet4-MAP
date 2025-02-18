import matplotlib.pyplot as plt


edges = [(u, v, w) for u in graph for v, w in graph[u].items()]

def bellman_ford(graph, edges, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parents = {node: None for node in graph}


    for _ in range(len(graph) - 1):
        for u, v, w in edges:
            if distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                parents[v] = u


    for u, v, w in edges:
        if distances[u] + w < distances[v]:
            raise ValueError("Cycle négatif détecté !")

    return distances, parents


def reconstruct_path(parents, target):
    path = []
    while target is not None:
        path.append(target)
        target = parents[target]
    return path[::-1]



