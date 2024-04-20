from sys import argv
from collections import deque
import functools

def find_start(grid: [[str]]) -> ((int, int), (int, int)):
    l = [None, None]
    for y, row in enumerate(grid):
        if 'S' in row:
            x = row.index('S')
            l[0] = y, x
            grid[y][x] = 'a'
        if 'E' in row:
            x = row.index('E')
            l[1] = y, x
            grid[y][x] = 'z'
    return tuple(l)            

cache = dict()
def neighbors(grid: [[str]], pos: (int, int)) -> [(int, int)]:
    global cache
    if pos not in cache:
        y, x = pos
        ns = []
        if y > 0:
            ns.append((y - 1, x))
        if y < len(grid) - 1:
            ns.append((y + 1, x))
        if x > 0:
            ns.append((y, x - 1))
        if x < len(grid[0]) - 1:
            ns.append((y, x + 1))
        cache[pos] = ns
    return cache[pos]

@functools.cache
def reachable(a: (int, int), b: (int, int)) -> bool:
    return ord(grid[a[0]][a[1]]) + 1 >= ord(grid[b[0]][b[1]])

def bfs(grid: [[str]], start: (int, int), end: (int, int)) -> int:
    q = deque()
    q.append((start, 0))
    visited = set()
    visited.add(start)
    while q:
        pos, length = q.popleft()
        if pos == end:
            return length
        for n in neighbors(grid, pos):
            if reachable(n, pos) and n not in visited:
                visited.add(n)
                q.append((n, length + 1))

def find_as(grid: [[str]]):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'a':
                yield (y, x)

def find_shortest_route(grid: [[str]], end: (int, int)) -> int:
    shortest = 1e6
    for start in find_as(grid):
        length = bfs(grid, end, start)
        if length is not None and length < shortest:
            shortest = length
    return shortest

grid = [list(line.strip()) for line in open(argv[1]).readlines()]
start, end = find_start(grid)
print(bfs(grid, end, start))
print(find_shortest_route(grid, end))
