from sys import argv
from math import gcd, atan, degrees

def get_occupied(grid: [[str]]) -> set:
    occupied = set()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '#':
                occupied.add((y, x))
    return occupied

def slope(p1: (int, int), p2: (int, int)) -> (int, int):
    dy, dx = p1[0] - p2[0], p1[1] - p2[1]
    if dy != 0 and dx != 0:
        factor = gcd(abs(dy), abs(dx))
        dy /= factor
        dx /= factor
    elif dy == 0:
        dx /= abs(dx)
    elif dx == 0:
        dy /= abs(dy)
    return int(dy), int(dx)

def get_slopes(occupied: set, origin: (int, int)) -> (set, {(int, int): [(int, int)]}):
    slopes = set()
    map = dict()
    for pos in occupied:
        if pos != origin:
            s = slope(pos, origin)
            slopes.add(s)
            if s not in map:
                map[s] = set()
            map[s].add(pos)
    return slopes, map

def manhattan(p1: (int, int), p2: (int, int)) -> int:
    return sum(abs(a - b) for a, b in zip(p1, p2))

def laser(points: {(int, int): [(int, int)]}, total: int, n: int) -> int:
    def clockwise(slope: (int, int)):
        dy, dx = slope
        if dy == 0 or dx == 0:
            return 90 * [(-1, 0), (0, 1), (1, 0), (0, -1)].index(slope)
        offset = 0
        if dy <= 0 and dx >= 0:
            dy, dx = dx, abs(dy)
            offset = 0
        elif dy >= 0 and dx >= 0:
            dy, dx = abs(dy), dx
            offset = 90
        elif dy >= 0 and dx <= 0:
            dy, dx = abs(dx), dy
            offset = 180
        else:
            dy, dx = abs(dy), abs(dx)
            offset = 270
        return offset + degrees(atan(dy/dx))
    num_removed = 0
    i = 0
    while True:
        ordered = sorted(points.keys(), key=clockwise)
        slope = ordered[i % len(points)]
        gone = points[slope].pop(0)
        if num_removed == n - 1:
            return gone[1] * 100 + gone[0]
        if len(points[slope]) == 0:
            points.pop(slope)
            i -= 1
        i += 1
        num_removed += 1

grid = [list(line.strip()) for line in open(argv[1]).readlines()]
occupied = get_occupied(grid)
colinears = {pos: get_slopes(occupied, pos) for pos in occupied}
best_station = max(colinears.keys(), key=lambda k: len(colinears[k][0]))
most_visible = max(len(s[0]) for s in colinears.values())
print(most_visible)
points = colinears[best_station][1]
points = {k: sorted(v, key=lambda p: manhattan(p, best_station)) for k, v in points.items()}
print(laser(points, len(occupied), 200))
