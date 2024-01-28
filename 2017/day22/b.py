from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

def parse_grid(lines: [str]) -> [[int]]:
    return [[2 if ch == '#' else 0 for ch in row.strip()] for row in lines]

def print_grid(grid: [[int]], pos):
    s = '.w#f'
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if y == pos[0] and x == pos[1]:
                print('[' + s[col], end=']')
            else:
                print(' %s ' % s[col], end='')
        print()

def burst(grid: [[int]], pos: (int, int), dir: int) -> ((int, int), int):
    deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    cell = grid[pos[0]][pos[1]]
    grid[pos[0]][pos[1]] = (cell + 1) % 4
    dir = (dir - 1 + cell) % 4
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
    return int(cell == 1), pos, dir

def simulate(grid: [[int]], bursts: int) -> int:
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
