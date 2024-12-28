from sys import argv
from heapq import heappush, heappop
from itertools import combinations

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

def find_best_path(grid: [[str]], start: (int, int), end: (int, int)) -> int:
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    q = []
    heappush(q, (0, start, 1, [start]))
    visited = set()
    while q:
        score, pos, dir, path = heappop(q)
        if pos == end:
            return score, path
        for i in (0, -1, 1):
            d = (dir + i) % len(directions)
            new_pos = add(pos, directions[d])
            if at(grid, new_pos) == '.' and (new_pos, d) not in visited:
                visited.add((new_pos, d))
                heappush(q, (score + 1 + 1000 * abs(i), new_pos, d, list(path) + [new_pos]))

def both_ways_exist(grid: [[str]], p1: (int, int), p2: (int, int)) -> (bool, {(int, int)}):
    y1, x1 = p1
    y2, x2 = p2
    visited = set()
    ys, xs = min(y1, y2), min(x1, x2)
    ye, xe = max(y1, y2), max(x1, x2)

    if ys == ye or xs == xe:
        return False, None

    # right
    for x in range(xs, xe + 1):
        if grid[ys][x] != '.':
            return False, None
        visited.add((ys, x))
    # down
    for y in range(ys + 1, ye + 1):
        if grid[y][xe] != '.':
            return False, None
        visited.add((y, xe))
    # left
    for x in range(xe - 1, xs - 1, -1):
        if grid[ye][x] != '.':
            return False, None
        visited.add((ye, x))
    # up
    for y in range(ye - 1, ys, -1):
        if grid[y][xs] != '.':
            return False, None
        visited.add((y, xs))
    return True, visited

def diff(p1: (int, int), p2: (int, int)) -> (int, int):
    return tuple(abs(a - b) for a, b in zip(p1, p2))

def aligned(p1: (int, int), p2: (int, int), path: [(int, int)]) -> bool:
    def get_diffs(pos: (int, int)) -> ((int, int), (int, int)):
        i = path.index(pos)
        prev = path[i-1]
        next = path[i+1]
        return diff(pos, prev), diff(pos, next)
    return sum(int(dy != 0 and dx == 0) for dy, dx in get_diffs(p1) + get_diffs(p2)) != 2

def find_all_points_on_a_best_path(grid: [[str]], best_path: [(int, int)]) -> int:
    '''only works on inputs where detours are other 2 edges of square'''
    all_points = set(best_path)
    for (y1, x1), (y2, x2) in combinations(best_path, 2):
        if abs(y2 - y1) + abs(x2 - x1) < 50:
            yes, visited = both_ways_exist(grid, (y1, x1), (y2, x2))
            if yes and aligned((y1, x1), (y2, x2), best_path):
                all_points.update(visited)
    return len(all_points)

def print_grid(grid: [[str]], path: [(int, int)]):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (y, x) in path:
                print('O', end='')
            else:
                print(cell, end='')
        print(flush=True)

grid = [list(line.strip()) for line in open(argv[1]).readlines()]
end = (1, len(grid[0]) - 2)
start = (len(grid) - 2, 1)
update(grid, end, '.')
update(grid, start, '.')
best_score, path = find_best_path(grid, start, end)
print(best_score)
#print_grid(grid, path)
print(find_all_points_on_a_best_path(grid, path))
