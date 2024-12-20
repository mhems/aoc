from sys import argv
from functools import cache

def find_start(grid: [[str]]) -> (int, int):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '^':
                grid[y][x] = '.'
                return y, x

@cache
def add(pos: (int, int), delta: (int, int)) -> (int, int):
    return tuple(map(sum, zip(pos, delta)))

def walk(grid: [[str]], start: (int, int), dir: int) -> [((int, int), int)]:
    '''Return # of points in path if exits grid, else -1 if a loop'''
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    seen = {(start, dir)}
    Y, X = len(grid), len(grid[0])
    pos = start
    while True:
        new_pos = add(pos, directions[dir])
        y, x = new_pos
        if 0 <= y < Y and 0 <= x < X:
            if grid[y][x] == '.':
                if (new_pos, dir) in seen:
                    return -1
                pos = new_pos
                seen.add((pos, dir))
            else:
                dir = (dir + 1) % 4
        else:
            return {step for step, _ in seen}

def find_obstructions(grid: [[str]], start: (int, int), dir: int, path: [((int, int), int)]) -> int:
    obstructions = set()
    for (y, x) in path:
        grid[y][x] = '#'
        if walk(grid, start, dir) == -1:
            obstructions.add((y, x))
        grid[y][x] = '.'
    return len(obstructions)

grid = [list(line.strip()) for line in open(argv[1]).readlines()]
start = find_start(grid)
path = walk(grid, start, 0)
print(len(path))
print(find_obstructions(grid, start, 0, path))
