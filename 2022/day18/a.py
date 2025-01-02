from sys import argv
from collections import deque

def neighbors(pos: (int, int, int), bounds: (int, int, int)) -> [(int, int, int)]:
    deltas = [(0, 0, 1), (0, 0, -1), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]
    x, y, z = pos
    return [(x + dx, y + dy, z + dz) for dx, dy, dz in deltas
            if 0 <= x + dx <= bounds[0] and 0 <= y + dy <= bounds[1] and 0 <= z + dz <= bounds[2]]

def num_neighbors(pos: (int, int, int), collection: {(int, int, int)}, bounds: (int, int, int)) -> int:
    return sum(int(neighbor in collection) for neighbor in neighbors(pos, bounds))

def surface_area(positions: [(int, int, int)], bounds: (int, int, int)) -> int:
    return sum(6 - num_neighbors(pos, positions, bounds) for pos in positions)

def flood(positions: {(int, int, int)}, start: (int, int), bounds: (int, int, int)) -> {(int, int, int)}:
    q = deque([start])
    visited = {start}
    while q:
        pos = q.popleft()
        for n in neighbors(pos, bounds):
            if n not in positions and n not in visited:
                visited.add(n)
                q.append(n)
    return visited

def flood_fill(positions: {(int, int, int)}, bounds: (int, int, int)) -> [{(int, int, int)}]:
    pockets = []
    visited = set()
    for x in range(bounds[0]):
        for y in range(bounds[1]):
            for z in range(bounds[2]):
                pos = (x, y, z)
                if pos not in visited and pos not in positions:
                    pocket = flood(positions, pos, bounds)
                    visited.update(pocket)
                    if (0, 0, 0) not in pocket:
                        pockets.append(pocket)
    return pockets    

def exterior_surface_area(positions: {(int, int, int)}, bounds: (int, int, int)):
    return sum(surface_area(pocket, bounds) for pocket in flood_fill(positions, bounds))

positions = frozenset(tuple(map(int, line.strip().split(','))) for line in open(argv[1]).readlines())
bounds = tuple(max(pos[dim] for pos in positions) + 1 for dim in range(3))
sa = surface_area(positions, bounds)
print(sa)
print(sa - exterior_surface_area(positions, bounds))
