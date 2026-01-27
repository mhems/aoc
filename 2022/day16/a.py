from sys import argv
from collections import deque
from itertools import combinations
from tqdm import tqdm

def parse() -> ({str: {str}}, {str: int}):
    adj = dict()
    flows = dict()
    for line in open(argv[1]).readlines():
        tokens = line.strip().replace('=', ' ').replace(';', '').split()
        flow = int(tokens[5])
        if flow > 0:
            flows[tokens[1]] = flow
        adj[tokens[1]] = set(''.join(tokens[10:]).split(','))
    return adj, flows

def bfs(graph: {str: {str}}, start: str, end: str) -> int:
    q = deque([(start, 0)])
    visited = {start}
    while q:
        cur, length = q.popleft()
        if cur == end:
            return length
        for n in graph[cur]:
            if n not in visited:
                visited.add(n)
                q.append((n, length + 1))
   
def all_pairs_distances(graph: {str: {str}}, valves: {str}) -> {(str, str): int}:
    distances = {}
    for u, v in combinations(valves, 2):
        distances[(u, v)] = bfs(graph, u, v)
        distances[(v, u)] = distances[(u, v)]
    return distances

graph, valves = parse()
ids = {key: 1 << i for i, key in enumerate(valves.keys())}
all_ids = (1 << len(valves.keys())) - 1
distances = all_pairs_distances(graph, valves.keys() | {'AA'})

def part1(mask: int = all_ids, time: int = 30) -> int:
    q = deque([('AA', 0, 0, time)])
    visited = dict()
    best = 0
    subset = {k: v for k, v in valves.items() if ids[k] & mask}
    while q:
        cur, total, opened, time_remaining = q.popleft()
        best_so_far = visited.get(time_remaining)
        if best_so_far is not None:
            if total < best_so_far:
                continue
        visited[time_remaining] = total
        if time_remaining <= 0 or opened == mask:
            if total > best:
                best = total
            continue
        for v in subset.keys():
            if v != cur and ids[v] & opened == 0:
                distance = distances[(cur, v)]
                if distance <= time_remaining:
                    q.append((v, total + subset[v] * (time_remaining - 1 - distance), opened | ids[v], time_remaining - 1 - distance))
    return best

def part2() -> int:
    answers = [(i, part1(i, 26)) for i in tqdm(range(all_ids + 1))]
    best = 0
    for k, v in tqdm(answers[:len(answers)//2 + 1]):
        for i, j in answers:
            if k & i == 0:
                total = v + j
                if total > best:
                   best = total
    return best

print(part1())
print(part2())
