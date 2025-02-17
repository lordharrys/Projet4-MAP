import matplotlib.pyplot as plt

graph = {
    1: {2: 4, 3: 2},
    2: {3: 5, 4: 10},
    3: {4: 3},
    4: {}
}

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

source = 1
try:
    distances, parents = bellman_ford(graph, edges, source)
except ValueError as e:
    print(e)
    exit()


def reconstruct_path(parents, target):
    path = []
    while target is not None:
        path.append(target)
        target = parents[target]
    return path[::-1]

# Calcul des chemins
paths = {node: reconstruct_path(parents, node) for node in graph if node != source}
distances = {node: distances[node] for node in graph}

print(distances)


