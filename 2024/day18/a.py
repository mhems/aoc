from sys import argv
from heapq import heappush, heappop

def build_grid(coords: [(int, int)], N: int, amt: int) -> [[str]]:
    grid = []
    for _ in range(N):
        grid.append([False] * N)
    for x, y in coords[:amt]:
        grid[y][x] = True
    return grid

def print_grid(grid: [[str]], points_in_path: {(int, int)} = None):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                print('#', end='')
            elif points_in_path and (y, x) in points_in_path:
                print('O', end='')
            else:
                print('.', end='')
        print()

def neighbors(pos: (int, int), Y: int, X: int) -> [(int, int)]:
    deltas = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    return [(pos[0] + dy, pos[1] + dx) for dy, dx in deltas
            if (0 <= pos[0] + dy < Y) and (0 <= pos[1] + dx < X)]

def vacant_neighbors(pos: (int, int), grid: [[str]], Y: int, X: int) -> [(int, int)]:
    return [(y, x) for y, x in neighbors(pos, Y, X) if grid[y][x] == False]

def taxicab(a: (int, int), b: (int, int)) -> int:
    return sum(abs(i - j) for i, j in zip(a, b))

def h(pos: (int, int), goal: (int, int)) -> int:
    return taxicab(pos, goal)

def reconstruct_path_length(came_from: {(int, int): (int, int)}, current: (int, int)) -> int:
    count = 1
    while current in came_from.keys():
        current = came_from[current]
        count += 1
    return count

def a_star(grid: [[str]], start: (int, int), end: (int, int)) -> int:
    open_set = []
    came_from = dict()
    g_score = dict()
    g_score[start] = 0
    f_score = dict()
    f_score[start] = h(start, end)
    heappush(open_set, (f_score[start], start))
    
    while open_set:
        _, current = heappop(open_set)
        if current == end:
            return reconstruct_path_length(came_from, current)
        for n in vacant_neighbors(current, grid, N, N):
            tentative_g_score = (g_score[current] if current in g_score else 1e6) + 1
            if tentative_g_score < (g_score[n] if n in g_score else 1e6):
                came_from[n] = current
                g_score[n] = tentative_g_score
                f_score[n] = tentative_g_score + h(n, end)
                if n not in set(e for _, e in open_set):
                    heappush(open_set, (f_score[n], n))
    return None

def find_first_blocker(grid: [[str]],
                       start: (int, int),
                       end: (int, int),
                       rest: [(int, int)]) -> (int, int):
    for x, y in rest:
        grid[y][x] = True
        if not a_star(grid, start, end):
            return x, y

coords = [tuple(map(int, line.strip().split(','))) for line in open(argv[1]).readlines()]
N, amt = (71, 1024) if argv[1] == 'input.txt' else (7, 12)
grid = build_grid(coords, N, amt)
#print_grid(grid)
#print(flush=True)
start, end = (0, 0), (N-1, N-1)
path_length = a_star(grid, start, end)
print(path_length - 1, flush=True)
print(','.join(map(str, find_first_blocker(grid, start, end, coords[amt:]))))
