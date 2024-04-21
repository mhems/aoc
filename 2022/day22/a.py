from sys import argv
import re

def add(p1: (int, int), p2: (int, int)) -> (int, int):
    return tuple(a + b for a, b in zip(p1, p2))

def at(grid: [[str]], pos: (int, int)) -> str:
    if pos[0] >= len(grid) or pos[1] >= len(grid[0]):
        return None
    return grid[pos[0]][pos[1]]

def wrap(grid: [[str]], pos: (int, int), facing: int) -> (int, int):
    y, x = pos
    if facing not in range(4):
        raise ValueError('unexpected facing: ' + facing)
    if facing == 0:
        x = 0
        while grid[y][x] == ' ':
            x += 1
    elif facing == 2:
        x = len(grid[0]) - 1
        while grid[y][x] == ' ':
            x -= 1
    elif facing == 1:
        y = 0
        while grid[y][x] == ' ':
            y += 1
    else:
        y = len(grid) - 1
        while grid[y][x] == ' ':
            y -= 1
    return (y, x)

def move(grid: [[str]], pos: (int, int), facing: int, amt: int):
    count = 0
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    delta = deltas[facing]
    while count < amt and at(grid, add(pos, delta)) == '.':
        pos = add(pos, delta)
        count += 1
    next = at(grid, add(pos, delta))
    if count == amt or next == '#':
        return pos
    if next in (None, ' '):
        a = wrap(grid, pos, facing)
        return pos if at(grid, a) == '#' else move(grid, a, facing, amt - count)
    raise ValueError('unexpected state: ' + next)

def walk(grid: [[str]], path) -> int:
    pos = (0, grid[0].index('.'))
    facing = 0
    for step in path:
        if isinstance(step, int):
            pos = move(grid, pos, facing, step)
        else:
            if step == 'L':
                facing = (facing - 1) % 4
            else:
                facing = (facing + 1) % 4
    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + facing

grid, steps = open(argv[1]).read().split('\n\n')
grid = [list(row) for row in grid.split('\n')]
width = max(len(row) for row in grid)
grid = [row + [' '] * (width - len(row)) for row in grid]
path = list(map(lambda e: int(e) if e[0].isdigit() else e, re.findall(r'\d+|[LR]', steps.strip())))
print(walk(grid, path))
