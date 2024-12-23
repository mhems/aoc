from sys import argv
from itertools import combinations
from collections import defaultdict

def build_graph(edges: [(str, str)]) -> ({str}, {(str, str)}, {str: {str}}):
    vertices, neighbors = set(), defaultdict(set)
    for u, v in edges:
        vertices.add(u)
        vertices.add(v)
        neighbors[u].add(v)
        neighbors[v].add(u)
    return vertices, neighbors

def num_triangles(vertices: {str}, neighbors: {str: {str}}) -> int:
    return sum(int(b in neighbors[a] and c in neighbors[a] and c in neighbors[b])
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
                inner(r | {v}, (p - skip) & neighbors[v], x & neighbors[v])
                skip.add(v)
                x.add(v)
    inner(set(), vertices, set())
    return answer
    
vertices, neighbors = build_graph(line.strip().split('-') for line in open(argv[1]).readlines())
print(num_triangles(vertices, neighbors))
print(','.join(sorted(bron_kerbosh(vertices, neighbors))))
