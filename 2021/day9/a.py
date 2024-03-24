from sys import argv
from collections import deque
from math import prod

def neighbors(grid: [[int]], pos: (int, int)) -> [int]:
    ps = [tuple(a + b for a, b in zip(pos, delta))
          for delta in ((0, -1), (0, 1), (1, 0), (-1, 0))]
    return [p for p in ps
            if 0 <= p[0] < len(grid) and 0 <= p[1] < len(grid[0])]

def risk_levels(grid: [[int]]) -> [int]:
    total = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell < min(grid[p[0]][p[1]] for p in neighbors(grid, (y, x))):
                total += cell + 1
    return total

def expand_basin(grid: [[int]], pos: (int, int)) -> {(int, int)}:
    q = deque()
    q.append(pos)
    visited = set()
    visited.add(pos)
    while q:
        cur = q.popleft()
        for n in neighbors(grid, cur):
            if grid[n[0]][n[1]] != 9 and n not in visited:
                visited.add(n)
                q.append(n)
    return visited

def find_basins(grid: [[int]]) -> int:
    basins = []
    explored = set()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != 9 and (y, x) not in explored:
                basin = expand_basin(grid, (y, x))
                for pos in basin:
                    explored.add(pos)
                basins.append(basin)
    by_size = sorted(basins, key=lambda b: len(b), reverse=True)
    return prod(len(b) for b in by_size[:3])

grid = [list(map(int, line.strip())) for line in open(argv[1]).readlines()]
print(risk_levels(grid))
print(find_basins(grid))
