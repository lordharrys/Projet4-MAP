import heapq as hp

def dijkstra(V, adj, s, t):
    edgeTo = {}
    distTo = {}
    for v in V:
        edgeTo[v] = None
        distTo[v] = float('inf')
    distTo[s] = 0.0

    pq = []
    hp.heappush(pq, (0.0, s))

    while pq:
        dist, v = hp.heappop(pq)
        if v == t:
            break

        for e in adj[v]:
            w = e.w
            if distTo[w] > distTo[v] + e.weight:
                distTo[w] = distTo[v] + e.weight
                edgeTo[w] = e
                hp.heappush(pq, (distTo[w], w))

    path = []
    if distTo[t] == float('inf'):
        return path

    current = t
    while current != s:
        path.append(current)
        current = edgeTo[current].v
    path.append(s)
    path.reverse()

    return path


class directed_edge:
    def __init__(self, v, w, weight):
        self.v = v
        self.w = w
        self.weight = weight