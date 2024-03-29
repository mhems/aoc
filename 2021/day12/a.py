from sys import argv
from collections import defaultdict, deque

def build_graph(lines: [str]) -> {str: {str}}:
    graph = defaultdict(set)
    for line in lines:
        a, b = line.strip().split('-')
        if a == 'start' or b == 'end':
            graph[a].add(b)
        elif a == 'end' or b == 'start':
            graph[b].add(a)
        else:
            graph[a].add(b)
            graph[b].add(a)
    return graph

def traverse_caves(graph: {str: {str}}, allow_small: bool = False) -> int:
    q = deque()
    paths = set()
    for n in graph['start']:
        q.append((n, ['start', n], {n}, None))
    while q:
        node, path, visited, small_cave = q.popleft()
        if node == 'end':
            paths.add(tuple(path))
        else:
            for adj in graph[node]:
                if adj.isupper() or adj not in visited:
                    q.append((adj, list(path) + [adj], set(visited) | {adj}, small_cave))
                elif allow_small and not small_cave:
                    q.append((adj, list(path) + [adj], set(visited), True))
    return len(paths)

lines = open(argv[1]).readlines()
graph = build_graph(lines)
print(traverse_caves(graph))
print(traverse_caves(graph, True))