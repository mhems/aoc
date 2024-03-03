from sys import argv
from itertools import permutations
from collections import namedtuple as nt
from collections import deque

Graph = nt('Graph', ['start', 'end', 'vertices', 'edges'])

def directional_neighbors(grid: [[str]], pos: (int, int)) -> [(int, int)]:
    return neighbors(grid, pos)

def neighbors(grid: [[str]], pos: (int, int)) -> [(int, int)]:
    neighbors = []
    if pos[0] > 0 and grid[pos[0] - 1][pos[1]] != '#':
        neighbors.append((pos[0] - 1, pos[1]))
    if pos[0] < len(grid) - 1 and grid[pos[0] + 1][pos[1]] != '#':
        neighbors.append((pos[0] + 1, pos[1]))
    if pos[1] > 0 and grid[pos[0]][pos[1] - 1] != '#':
        neighbors.append((pos[0], pos[1] - 1))
    if pos[1] < len(grid[0]) - 1 and grid[pos[0]][pos[1] + 1] != '#':
        neighbors.append((pos[0], pos[1] + 1))
    return neighbors

def find_vertices(grid: [[str]]) -> {(int, int)}:
    vertices = set()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != '#' and len(neighbors(grid, (y, x))) > 2:
                vertices.add((y, x))
    return vertices

def walk(grid: [[str]],
         start: (int, int),
         end: (int, int),
         vertices: {(int, int)},
         visited: {(int, int)} = None) -> int:
    if visited is None:
        visited = set()
    pos = start
    visited.add(pos)
    steps = 0
    while True:
        ns = directional_neighbors(grid, pos)
        ns = set(ns) - visited
        if pos == end:
            return steps
        if len(ns) == 0:
            return None
        if len(ns) > 1:
            results = [walk(grid, n, end, vertices, visited) for n in ns]
            num_valid = [result for result in results if result is not None]
            if len(num_valid) > 0:
                assert len(num_valid) == 1
                return num_valid[0] + steps + 1
        pos = ns.pop()
        steps += 1
        if pos == end:
            return steps
        if pos in vertices:
            return None
        visited.add(pos)

def find_edges(grid: [[str]], vertices: {(int, int)}) -> {((int, int), (int, int)): int}:
    edges = {}
    for a, b in permutations(vertices, 2):
        steps = walk(grid, a, b, vertices)
        if steps is not None:
            edges[(a, b)] = steps
    return edges        

def make_graph(grid: [[str]]) -> Graph:
    start, end = (0, 1), (len(grid) - 1, len(grid[0]) - 2)
    vertices = find_vertices(grid)
    vertices.add(start)
    vertices.add(end)
    edges = find_edges(grid, vertices)
    return Graph(start, end, vertices, edges)

cache = {}
def adjacencies(graph: Graph, u: (int, int)) -> [(int, int)]:
    if u in cache:
        return cache[u]
    ret = [v for v in graph.vertices if v != u and (u, v) in graph.edges]
    cache[u] = ret
    return ret
               
def longest_path(graph: Graph) -> int:
    q = deque()
    q.append((graph.start, 0, set()))
    max_length = 0
    while len(q) > 0:
        cur, length, path = q.popleft()
        if cur == graph.end and length > max_length:
            max_length = length
            print(len(q), len(path), max_length)
        else:
            for adj in adjacencies(graph, cur):
                if adj not in path:
                    new_path = set(path)
                    new_path.add(adj)
                    q.append((adj, length + graph.edges[(cur, adj)], new_path))
    return max_length

with open(argv[1]) as fp:
    grid = [list(line.strip()) for line in fp.readlines()]

graph = make_graph(grid)
print(longest_path(graph))
