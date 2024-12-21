from sys import argv
from collections import deque
from functools import cache
from tqdm import tqdm

def build_gridmap(grid: [str]) -> ((int, int), (int, int), {(int, int)}, {(int, int)}):
    start = None
    end = None
    walls = set()
    path = set()
    Y, X = len(grid), len(grid[0])
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '#':
                if 0 < y < Y - 1 and 0 < x < X - 1:
                    walls.add((y, x))
            else:
                if cell == 'S':
                    start = (y, x)
                elif cell == 'E':
                    end = (y, x)
                path.add((y, x))
    return start, end, walls, path

@cache
def neighbors(pos: (int, int)) -> {(int, int)}:
    return {(pos[0] + dy, pos[1] + dx) for dy, dx in [(-1, 0), (0, -1), (0, 1), (1, 0)]}

def bfs(open: {(int, int)}, start: (int, int), end: (int, int)) -> int:
    q = deque()
    visited = set()
    q.append((start, 0))
    while q:
        pos, path = q.popleft()
        if pos == end:
            return path
        for n in neighbors(pos):
            if n in open and n not in visited:
                visited.add(n)
                q.append((n, path + 1))

def find_cheats(walls: {(int, int)}, open: {(int, int)}, start: (int, int), end: (int, int)) -> int:
    standard = bfs(open, start, end)
    return sum(int(standard - bfs(set(open) | {wall}, start, end) >= 100) for wall in tqdm(walls))

grid = [line.strip() for line in open(argv[1]).readlines()]
start, end, walls, path = build_gridmap(grid)
print(find_cheats(walls, path, start, end))
