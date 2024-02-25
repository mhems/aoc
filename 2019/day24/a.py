from sys import argv
from itertools import chain

def make_grid() -> [[int]]:
    return [[int(cell == '#') for cell in line.strip()] for line in open(argv[1]).readlines()]

def print_grid(grid: [[int]]):
    print('\n'.join(''.join('.#'[cell] for cell in row) for row in grid))

def num_bugs_adjacent(grid: [[int]], pos: (int, int)) -> int:
    num = 0
    if pos[0] > 0:
        num += grid[pos[0]-1][pos[1]]
    if pos[1] > 0:
        num += grid[pos[0]][pos[1]-1]
    if pos[0] < len(grid) - 1:
        num += grid[pos[0]+1][pos[1]]
    if pos[1] < len(grid[0]) - 1:
        num += grid[pos[0]][pos[1]+1]
    return num

def tick(grid: [[int]]) -> [[int]]:
    new_grid = [[0] * len(grid[0]) for _ in range(len(grid))]
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            n = num_bugs_adjacent(grid, (y, x))
            new_grid[y][x] = int(n == 1) if cell == 1 else int(1 <= n <= 2)
    return new_grid

def grid_to_tuple(grid: [[int]]) -> ((int)):
    return tuple(tuple(row) for row in grid)

def biodiversity(grid: [[int]]) -> int:
    return sum(2 ** i for i, v in enumerate(chain.from_iterable(grid)) if v == 1)

def cycle(grid: [[int]]) -> int:
    seen = set()
    seen.add(grid_to_tuple(grid))
    while True:
        grid = tick(grid)
        cur = grid_to_tuple(grid)
        if cur in seen:
            print_grid(grid)
            return biodiversity(grid)
        seen.add(cur)
    
grid = make_grid()
print(cycle(grid))
