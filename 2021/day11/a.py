from sys import argv

def neighbors(grid: [[int]], pos: (int, int)) -> [(int, int)]:
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    poses = [tuple(a + b for a, b in zip(pos, delta)) for delta in deltas]
    return [p for p in poses if 0 <= p[0] < len(grid) and 0 <= p[1] < len(grid[0])]

def flash(grid: [[int]], pos: (int, int), flashed: {(int, int)}):
    flashed.add(pos)
    for n in neighbors(grid, pos):
        grid[n[0]][n[1]] += 1
        if grid[n[0]][n[1]] > 9 and n not in flashed:
            flash(grid, n, flashed)
    grid[pos[0]][pos[1]] = 0

def step(grid: [[int]]) -> ([[int]], int):
    new_grid = [[c + 1 for c in row] for row in grid]
    flashed = set()
    for y, row in enumerate(new_grid):
        for x in range(len(row)):
            if new_grid[y][x] > 9:
                flash(new_grid, (y, x), flashed)
    for loc in flashed:
        new_grid[loc[0]][loc[1]] = 0
    return new_grid, len(flashed)

def cycle(grid: [[int]], n: int = 100):
    total = 0
    i = 0
    N = len(grid) * len(grid[0])
    while True:
        grid, t = step(grid)
        total += t
        i += 1

        if i == n:
            print(total)
        elif t == N:
            print(i)
            break

grid = [list(map(int, line.strip())) for line in open(argv[1]).readlines()]
cycle(grid)
