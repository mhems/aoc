from sys import argv
from collections import defaultdict

deltas = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1,))

def neighborsxd(pos: tuple, dim: int, include: bool) -> list[tuple]:
    w, z, y, x = pos
    if dim == 2: return [(w, z, y+dy, x+dx) for dy, dx in deltas if dy != 0 or dx != 0 or include]
    if dim == 3: return neighborsxd((w, z-1, y, x), 2, True) + neighborsxd((w, z, y, x), 2, include) + neighborsxd((w, z+1, y, x), 2, True)
    return neighborsxd((w-1, z, y, x), 3, True) + neighborsxd((w, z, y, x), 3, False) + neighborsxd((w+1, z, y, x), 3, True)

def conway(initial, dim: int):
    active = set(initial)
    for _ in range(6):
        new_active = set()
        neighboring_active = defaultdict(int)
        for cell in active:
            neighbors = neighborsxd(cell, dim, dim == 4)
            count = 0
            for neighbor in neighbors:
                count += int(neighbor in active)
                neighboring_active[neighbor] += 1
            if 2 <= count <= 3:
                new_active.add(cell)
        for n, amt in neighboring_active.items():
            if amt == 3:
                new_active.add(n)
        active = new_active
    return len(active)

active = {(0, 0, y, x) for y, row in enumerate(open(argv[1]).readlines()) for x, cell in enumerate(row.strip()) if cell == '#'}
print(conway(active, 3))
print(conway(active, 4))
