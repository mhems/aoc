from sys import argv
from collections import deque

def parse_grid(filename) -> [[str]]:
    with open(filename) as fp:
        return [list(line.rstrip('\n').replace(' ', '#')) for line in fp.readlines()]

def print_grid(grid: [[str]]):
    for row in grid:
        for cell in row:
            print(cell, end='')
        print()
    print()

def find_start(grid: [[str]]) -> (int, int):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'O':
                return (y, x)

def vacant_neighbors(grid: [[str]], pos: (int, int)) -> [(int, int)]:
    neighbors = []
    if pos[0] > 0:
        neighbors.append((pos[0] - 1, pos[1]))
    if pos[0] < len(grid) - 1:
        neighbors.append((pos[0] + 1, pos[1]))
    if pos[1] > 0:
        neighbors.append((pos[0], pos[1] - 1))
    if pos[1] < len(grid[0]) - 1:
        neighbors.append((pos[0], pos[1] + 1))
    return [(y, x) for y, x in neighbors if grid[y][x] != '#']

def floodfill(grid: [[str]], start: (int, int)) -> int:
    q = deque()
    q.append((start, 0))
    visited = set()
    while len(q) > 0:
        cur, time = q.popleft()
        for pos in vacant_neighbors(grid, cur):
            if pos not in visited:
                visited.add(pos)
                q.append((pos, time + 1))
    return time

grid = parse_grid(argv[1])
print(floodfill(grid, find_start(grid)))
