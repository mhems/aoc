from sys import argv
from itertools import combinations
from collections import defaultdict

def build_graph(edges: [(str, str)]) -> ({str}, {(str, str)}, {str: {str}}):
    vertices = set()
    edgeset = set()
    neighbors = defaultdict(set)
    for u, v in edges:
        edgeset.add((u, v))
        edgeset.add((v, u))
        vertices.add(u)
        vertices.add(v)
        neighbors[u].add(v)
        neighbors[v].add(u)
    return vertices, edgeset, neighbors

def num_triangles(vertices: {str}, edges: {(int, int)}) -> int:
    return sum(int((a, b) in edges and (b, c) in edges and (c, a) in edges)
               for a, b, c in (combo for combo in combinations(vertices, 3) if any(e[0] == 't' for e in combo)))

def bron_kerbosh(vertices: {str}, neighbors: {str: {str}}) -> {str}:
    answer = None
    def inner(r: {str}, p: {str},  x: {str}) -> {str}:
        nonlocal answer
        if len(p) == 0 and len(x) == 0:
            if answer is None or len(r) > len(answer):
                answer = r
        skip = set()
        for v in p:
            if v not in skip:
                ns = neighbors[v]
                inner(r | {v}, (p - skip) & ns, x & ns)
                skip.add(v)
                x.add(v)
    inner(set(), vertices, set())
    return answer
    
edges = [line.strip().split('-') for line in open(argv[1]).readlines()]
vertices, edge_set, neighbors = build_graph(edges)
print(num_triangles(vertices, edge_set))
print(','.join(sorted(bron_kerbosh(vertices, neighbors))))
