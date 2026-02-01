from sys import argv
import re
import numpy as np
from collections import defaultdict, deque
from typing import Set
import networkx as nx

slabs = [tuple(int(match.group(0)) for match in re.finditer(r'\d+', line.strip())) for line in open(argv[1]).readlines()]
mins = [100, 100, 100]
maxs = [0, 0, 0]
for slab in slabs:
    mins[0] = min(mins[0], slab[0])
    mins[1] = min(mins[1], slab[1])
    mins[2] = min(mins[2], slab[2])
    maxs[0] = max(maxs[0], slab[3])
    maxs[1] = max(maxs[1], slab[4])
    maxs[2] = max(maxs[2], slab[5])
size = tuple(a - b + 2 for a, b in zip(maxs, mins))
a = np.zeros((size[2], size[0], size[1]), dtype=np.uint16)
Z = size[2]

adjs = defaultdict(set)

for i, slab in enumerate(sorted(slabs, key = lambda slab: (slab[2], slab[5]))):
    x1, y1, z1, x2, y2, z2 = slab
    id = i + 1
    found = False
    min_z = Z - 1
    for z in range(Z - z1, Z):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                e = a[z, x, y]
                if e != 0:
                    adjs[int(e)].add(id)
                    found = True
                    min_z = z - 1
        if found:
            break
    for z in range(min_z, min_z - 1 - (z2 - z1), -1):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                a[z, x, y] = id

def num_would_fall(G, root: int) -> Set[int]:
    q = deque([root])
    fallen = {root}
    while q:
        cur = q.popleft()
        for n in G.succ[cur]:
            if len(set(G.pred[n]) - fallen) == 0:
                fallen.add(n)
                q.append(n)
    fallen.remove(root)
    return fallen

G = nx.DiGraph(adjs)
part1 = len(set(range(1, id + 1)) - set(G.nodes()))
part2 = 0
for k in G.nodes():
    v = len(num_would_fall(G, k))
    if v == 0:
        part1 += 1
    else:
        part2 += v
print(part1, part2)
