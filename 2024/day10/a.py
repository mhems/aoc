from sys import argv
from collections import deque
from functools import reduce

def neighbors(pos: (int, int), Y: int, X: int) -> {(int, int)}:
    return [(pos[0] + dy, pos[1] + dx) for dy, dx in [(0, -1), (0, 1), (1, 0), (-1, 0)]
            if 0 <= pos[0] + dy < Y and 0 <= pos[1] + dx < X]

def score(grid: [[int]], start: (int, int)) -> int:
    q = deque([start])
    peaks = set()
    rating = 0
    Y, X = len(grid), len(grid[0])
    while q:
        pos = q.popleft()
        v = grid[pos[0]][pos[1]]
        if v == 9:
            peaks.add(pos)
            rating += 1
        for n in neighbors(pos, Y, X):
            if v + 1 == grid[n[0]][n[1]]:
                q.append(n)
    return len(peaks), rating

def find_trailheads(grid: [[int]]) -> {(int, int)}:
    return {(y, x) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == 0}

grid = [[int(digit) for digit in line.strip()] for line in open(argv[1]).readlines()]
print(reduce(lambda t1, t2: tuple(map(sum, zip(t1, t2))),
             (score(grid, trailhead) for trailhead in find_trailheads(grid))))
