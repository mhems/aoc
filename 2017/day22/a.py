from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

def parse_grid(lines: [str]) -> [[bool]]:
    return [[ch == '#' for ch in row.strip()] for row in lines]

def print_grid(grid: [[bool]], pos):
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if y == pos[0] and x == pos[1]:
                print('[' + ('#' if col else '.'), end=']')
            elif col:
                print(' # ', end='')
            else:
                print(' . ', end='')
        print()

def burst(grid: [[bool]], pos: (int, int), dir: int) -> ((int, int), int):
    deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    cell = grid[pos[0]][pos[1]]
    dir = (dir + 1 if cell else dir - 1) % 4
    grid[pos[0]][pos[1]] = not cell
    pos = tuple(a + b for a, b in zip(pos, deltas[dir]))
    R, C = len(grid), len(grid[0])
    if pos[0] < 0:
        grid.insert(0, [False] * C)
        pos = (pos[0] + 1, pos[1])
    if pos[0] >= R:
        grid.append([False] * C)
    if pos[1] < 0:
        for row in grid:
            row.insert(0, False)
        pos = (pos[0], pos[1] + 1)
    if pos[1] >= C:
        for row in grid:
            row.append(False)
    return int(not cell), pos, dir

def simulate(grid: [[bool]], bursts: int) -> int:
    dir = 0
    pos = (len(grid)//2, len(grid[0])//2)
    count = 0
    for i in range(bursts):
        c, pos, dir = burst(grid, pos, dir)
        count += c
        #print_grid(grid, pos)
        #print('i', i, 'count', count, 'dir', 'NESW'[dir])
        #print()
    return count

grid = parse_grid(lines)
print(simulate(grid, int(argv[2])))
