from sys import argv
from heapq import heappush, heappop

at_cache = dict()
def at(grid: [[str]], pos: (int, int)) -> str:
    value = at_cache.get(pos, False)
    if value != False:
        return value
    y, x = pos
    if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
        at_cache[pos] = grid[y][x]
    else:
        at_cache[pos] = None
    return at_cache[pos]

def update(grid: [[str]], pos: (int, int), val: str):
    grid[pos[0]][pos[1]] = val

def add(pos: (int, int), delta: (int, int)) -> (int, int):
    return tuple(map(sum, zip(pos, delta)))

def find_best_path(grid: [[str]]) -> int:
    end = (1, len(grid[0]) - 2)
    start = (len(grid) - 2, 1)
    update(grid, end, '.')
    update(grid, start, '.')
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    q = []
    heappush(q, (0, start, 1))
    visited = set()
    while q:
        score, pos, dir = heappop(q)
        if pos == end:
            return score
        for i in (0, -1, 1):
            d = (dir + i) % len(directions)
            new_pos = add(pos, directions[d])
            if at(grid, new_pos) == '.' and (new_pos, d) not in visited:
                num_turns = abs(i)
                visited.add((new_pos, d))
                heappush(q, (score + 1 + 1000 * num_turns, new_pos, d))

def print_grid(grid: [[str]], path: [(int, int)]):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (y, x) in path:
                print('O', end='')
            else:
                print(cell, end='')
        print(flush=True)

grid = [list(line.strip()) for line in open(argv[1]).readlines()]
print(find_best_path(grid))
