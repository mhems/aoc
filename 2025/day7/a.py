import sys
from collections import defaultdict

def trace(grid: list[str],
          pos: tuple[int, int],
          parent: tuple[int, int],
          adj_list: dict[tuple[int, int], list[tuple[int, int]]]):
    y, x = pos
    if 0 <= x < len(grid[0]):
        while y < len(grid) and grid[y][x] != '^':
            y += 1
        if y < len(grid):
            adj_list[parent].append((y, x))
            if (y, x) not in adj_list.keys():
                trace(grid, (y, x-1), (y, x), adj_list)
                trace(grid, (y, x+1), (y, x), adj_list)

grid = [line.rstrip() for line in open(sys.argv[1]).readlines()]
start = (0, grid[0].index('S'))
adj_list = defaultdict(list)
trace(grid, start, start, adj_list)

cache = dict()
def count(start: tuple[int, int], adj_list: dict[tuple[int, int], list[tuple[int, int]]]) -> int:
    global cache
    if start not in cache:
        children = adj_list[start]
        if len(children) == 0:
            cache[start] = 2
        elif len(children) == 1:
            cache[start] = 1 + count(children[0], adj_list)
        else:
            cache[start] = count(children[0], adj_list) + count(children[1], adj_list)
    return cache[start]

n = count(start, adj_list) - 1
print(len(adj_list.keys()) - 1)
print(n)
