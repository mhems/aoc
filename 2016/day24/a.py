from sys import argv
from itertools import combinations, permutations
from tqdm import tqdm

with open(argv[1]) as fp:
    lines = fp.readlines()

def parse_grid(lines: [str]) -> ([[bool]], [(int, int)]):
    R, C = len(lines), len(lines[0].strip())
    nodes = [None] * 10
    grid = [[False] * C for _ in range(R)]
    for y in range(R):
        for x in range(C):
            cur = lines[y][x]
            if cur != '#':
                grid[y][x] = True
                if cur != '.':
                    nodes[int(cur)] = (y, x)
    return (grid, [node for node in nodes if node])

def neighbors(grid: [[bool]], x: int, y: int) -> [(int, int)]:
    poses = [(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x)]
    return [(y, x) for y, x in poses if grid[y][x]]

def make_graph(grid: [[bool]]) -> {(int, int): [(int, int)]}:
    vertices = {}
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
            if grid[y][x]:
                ns = neighbors(grid, x, y)
                if len(ns) > 0:
                    vertices[(y, x)] = ns
    return vertices

def path(prev: {(int, int): [(int, int)]},
         src: (int, int),
         dst: (int, int)) -> [(int, int)]:
    S, u = [], dst
    if prev[u] is not None or u == src:
        while u is not None:
            S.insert(0, u)
            u = prev[u]
    return S

def dijkstra(vertices: {(int, int): [(int, int)]},
             src: (int, int),
             dst: (int, int)) -> [(int, int)]:
    dist, prev, Q = {}, {}, []
    for vertex in vertices.keys():
        dist[vertex] = 2 ** 32
        prev[vertex] = None
        Q.append(vertex)
    dist[src] = 0
    while len(Q) > 0:
        u = min(((vertex, dist[vertex]) for vertex in Q),
                key=lambda pair: pair[1])[0]
        if u == dst:
            return path(prev, src, dst)
        Q.remove(u)
        for neighbor in vertices[u]:
            if neighbor in Q:
                alt = dist[u] + 1
                if alt < dist[neighbor]:
                    dist[neighbor] = alt
                    prev[neighbor] = u
    return []

grid, nodes = parse_grid(lines)
print(len(nodes), 'points of interest')
vertices = make_graph(grid)
print(len(vertices), 'vertices')
paths = {(src, dst): len(dijkstra(vertices, src, dst)) - 1
         for src, dst in tqdm(combinations(nodes, 2))}
s = ''.join(str(i) for i in range(1, len(nodes)))
orderings = ['0' + ''.join(permutation) for permutation in permutations(s)]
print(len(orderings), 'path permutations')
node_map = {i: node for i, node in enumerate(nodes)}

def weight_connection(src: str,
           dst: str,
           paths: {((int, int), (int, int)): int},
           node_map: {int, (int, int)}) -> int:
    src_node, dst_node = node_map[int(src)], node_map[int(dst)]
    if (src_node, dst_node) in paths:
        return paths[(src_node, dst_node)]
    return paths[(dst_node, src_node)]

def weight_path(path: str,
                paths: {((int, int), (int, int)): int},
                node_map: {int, (int, int)}) -> int:
    return sum(weight_connection(path[i], path[i+1], paths, node_map)
               for i in range(len(path) - 1))

def min_weight_path(paths: {((int, int), (int, int)): int},
                    node_map: {int, (int, int)},
                    orderings: [str]) -> int:
    return min(weight_path(path, paths, node_map) for path in orderings)

print('part1', min_weight_path(paths, node_map, orderings))
orderings2 = ['0' + ''.join(permutation) + '0' for permutation in permutations(s)]
print('part2', min_weight_path(paths, node_map, orderings2))
