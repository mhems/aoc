from sys import argv
from heapq import heappush, heappop
from functools import cache

ROCKY = 0
WET = 1
NARROW = 2

NEITHER = 0
TORCH = 1
ROPE = 2

def make_cave(X: int, Y: int, depth: int, target: (int, int)) -> [[int]]:
    indices = [[None] * (X+1) for _ in range(Y+1)]
    levels = [[None] * (X+1) for _ in range(Y+1)]
    types = [[None] * (X+1) for _ in range(Y+1)]
    indices[0][0] = 0
    levels[0][0] = depth % 20183
    for x in range(1, X+1):
        indices[0][x] = x * 16807
        levels[0][x] = (indices[0][x] + depth) % 20183
    for y in range(1, Y+1):
        indices[y][0] = y * 48271
        levels[y][0] = (indices[y][0] + depth) % 20183
    for y in range(1, Y+1):
        for x in range(1, X+1):
            if (y, x) == target:
                indices[y][x] = 0
            else:
                indices[y][x] = levels[y][x-1] * levels[y-1][x]
            levels[y][x] = (indices[y][x] + depth) % 20183
    for y in range(Y+1):
        for x in range(X+1):
            types[y][x] = levels[y][x] % 3
    return types

def print_cave(cave: [[int]], target: (int, int)):
    for y, row in enumerate(cave):
        for x, cell in enumerate(row):
            if (y, x) == target:
                print('G', end='')
            else:
                print('.=|'[cell], end='')
        print()

def risk_level(cave: [[int]], target: (int, int)) -> int:
    return sum(sum(cell for x, cell in enumerate(row) if x <= target[1]) for y, row in enumerate(cave) if y <= target[0])

@cache
def neighbors(pos: (int, int), width: int, height: int) -> [(int, int)]:
    ps = [(pos[0] + dy, pos[1] + dx) for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]]
    return [(y, x) for y, x in ps if 0 <= x < width and 0 <= y < height]

@cache
def dist(p1: (int, int), p2: (int, int)) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find(cave: [[str]], end: (int, int)) -> int:
    q = []
    X, Y = len(cave[0]), len(cave)
    heappush(q, (0, 0, (0, 0), TORCH))
    visited = {((0, 0), TORCH)}
    allowed = {ROCKY: {TORCH, ROPE}, WET: {NEITHER, ROPE}, NARROW: {NEITHER, TORCH}}
    lookup = {
        (ROCKY, TORCH): [ROPE],
        (ROCKY, ROPE): [TORCH],
        (ROCKY, NEITHER): [TORCH, ROPE],
        (WET, TORCH): [NEITHER, ROPE],
        (WET, ROPE): [NEITHER],
        (WET, NEITHER): [ROPE],
        (NARROW, TORCH): [NEITHER],
        (NARROW, ROPE): [NEITHER, TORCH],
        (NARROW, NEITHER): [TORCH]
    }
    
    while q:
        _, time, pos, tool = heappop(q)
        if pos == end and tool == TORCH:
            return time
        climate = cave[pos[0]][pos[1]]
        d = dist(pos, end)
        for candidate in lookup[(climate, tool)]:
            if (time + 7, pos, candidate) not in visited:
                visited.add((time + 7, pos, candidate))
                heappush(q, (time + 7 + d, time + 7, pos, candidate))
        for n in neighbors(pos, X, Y):
            if tool in allowed[cave[n[0]][n[1]]] and (time + 1, n, tool) not in visited:
                visited.add((time + 1, n, tool))
                heappush(q, (time + 1 + dist(n, end), time + 1, n, tool))

lines = open(argv[1]).readlines()
depth = int(lines[0].split()[1])
target = tuple(reversed(list(map(int, lines[1].split()[1].split(',')))))
cave = make_cave(target[1] * 3, target[0] + 20, depth, target)
#print_cave(cave, target)
print(risk_level(cave, target))
print(find(cave, target))
