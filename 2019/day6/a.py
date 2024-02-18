from sys import argv
from collections import deque

def make_graph(lines: [str]) -> {str: [str]}:
    adj = {}
    for line in lines:
        a, b = line.split(')')
        if a not in adj:
            adj[a] = []
        if b not in adj:
            adj[b] = []
        adj[a].append(b)
        adj[b].append(a)
    return adj

def bfs(adj: {str: [str]}, goal: str, start: str = 'COM') -> int:
    q = deque()
    q.append((start, 0))
    visited = set()
    visited.add(start)
    while len(q) > 0:
        cur, length = q.popleft()
        if cur == goal:
            return length
        for neighbor in adj[cur]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append((neighbor, length + 1))  

lines = [line.strip() for line in open(argv[1]).readlines()]
adj = make_graph(lines)
print(sum(bfs(adj, node) for node in adj.keys()))
print(bfs(adj, 'YOU', 'SAN') - 2)
