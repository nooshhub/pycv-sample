import heapq
import math

graph = {
    "A": {"B": 5, "C": 1},
    "B": {"A": 5, "C": 2, "D": 1},
    "C": {"A": 1, "B": 2, "D": 4, "E": 8},
    "D": {"B": 1, "C": 4, "E": 3, "F": 6},
    "E": {"C": 8, "D": 3},
    "F": {"D": 6},
}


def init_distance(graph, s):
    distance = {s: 0}
    for vertex in graph:
        if vertex != s:
            distance[vertex] = math.inf
    return distance


def dijkstra(graph, s):
    pqueue = []
    heapq.heappush(pqueue, (0, s))
    seen = set()
    parent = {s: None}
    distance = init_distance(graph, s)

    while (len(pqueue) > 0):
        pair = heapq.heappop(pqueue)
        dist = pair[0]
        vertex = pair[1]
        seen.add(vertex)

        nodes = graph[vertex].keys()
        for w in nodes:
            if w not in seen:
                w_dist = dist + graph[vertex][w]
                if w_dist < distance[w]:
                    heapq.heappush(pqueue, (w_dist, w))
                    parent[w] = vertex
                    distance[w] = w_dist
    return parent, distance


def get_nodes(parent, e):
    nodes = [e]

    while parent[e] is not None:
        e = parent[e]
        nodes.append(e)
    return nodes


if __name__ == '__main__':
    parent, distance = dijkstra(graph, "A")
    print(parent)
    print(distance)
    print(get_nodes(parent, 'F'))

    # pqueue = []
    # heapq.heappush(pqueue, (1, 'A'))
    # heapq.heappush(pqueue, (7, 'B'))
    # heapq.heappush(pqueue, (3, 'C'))
    # heapq.heappush(pqueue, (6, 'D'))
    # heapq.heappush(pqueue, (2, 'E'))
    # print(heapq.heappop(pqueue))
    # print(heapq.heappop(pqueue))
    # print(heapq.heappop(pqueue))
    # print(heapq.heappop(pqueue))
    # print(heapq.heappop(pqueue))
    # print(heapq.heappop(pqueue))
