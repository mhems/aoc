from sys import argv
from collections import deque
from itertools import permutations

def parse() -> ({str: (int, {str})}):
    adj = dict()
    for line in open(argv[1]).readlines():
        tokens = line.strip().replace('=', ' ').replace(';', '').split()
        adj[tokens[1]] = int(tokens[5]), set(''.join(tokens[10:]).split(','))
    return adj

def bfs(graph: {str: (int, {str})}, start: str, end: str) -> int:
    q = deque()
    visited = set()
    q.append((start, 0))
    visited.add(start)
    while q:
        cur, length = q.popleft()
        if cur == end:
            return length
        for n in graph[cur][1]:
            if n not in visited:
                visited.add(n)
                q.append((n, length + 1))
   
def all_pairs_distances(graph: {str: (int, {str})}, valves: {str}) -> {(str, str): int}:
    distances = {}
    for u, v in permutations(valves, 2):
        distances[(u, v)] = bfs(graph, u, v)
        distances[(v, u)] = distances[(u, v)]
    return distances

def psearch(graph: {str: (int, int)}, valves: {str}, distances: {(str, str): int}, time: int) -> int:
    q = deque()
    def enqueue(cur: str, next: str, visited: [int], initial_pressure: int, remaining_valves: {int}, remaining_time: int):
        nonlocal q, distances, graph
        left = distances[(cur, next)] + 1
        minute = remaining_time - left
        q.append((next, list(visited) + [next], set(remaining_valves) - {next}, initial_pressure + graph[next][0] * minute, minute))
    biggest = 0
    for valve in valves:
        enqueue('AA', valve, [], 0, valves, time)
    while q:
        cur, visited, todo, pressure, togo = q.popleft()
        if len(todo) == 0 or togo <= 0:
            if pressure > biggest:
                biggest = pressure
            continue
        for v in todo:
            enqueue(cur, v, visited, pressure, todo, togo)
    return biggest

def find_max_pressure(graph: {str: (int, {str})}, time: int = 30) -> int:
    valves = {v for v, (rate, _) in graph.items() if rate > 0}
    distances = all_pairs_distances(graph, valves | {'AA'})
    return psearch(graph, valves, distances, time)

graph = parse()
print(find_max_pressure(graph))
