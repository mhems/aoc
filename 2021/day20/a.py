from sys import argv
from operator import or_
from functools import reduce

def make_grid(lines: [str]) -> [[bool]]:
    return [[c == '#' for c in row] for row in lines]

def get_light_locations(algorithm: str) -> {int}:
    assert len(algorithm) == 512
    return set(i for i, ch in enumerate(algorithm) if ch == '#')

def get_value(grid: [[bool]], pos: (int, int), lights: {int}) -> bool:
    deltas = [(1, 1), (1, 0), (1, -1), (0, 1), (0, 0), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
    ps = [tuple(sum(t) for t in zip(pos, delta)) for delta in deltas]
    return reduce(or_, (int(grid[p[0]][p[1]]) << i for i, p in enumerate(ps))) in lights

def num_lit(grid: [[bool]]) -> int:
    return sum(sum(int(cell) for cell in row) for row in grid)

def print_grid(grid: [[bool]]):
    for row in grid:
        for cell in row:
            print('#' if cell else '.', end='')
        print()
    print()

def pad(grid: [[bool]], value: bool = False, n: int = 2) -> [[bool]]:
    if value:
        grid[0] = [True] * len(grid[0])
        grid[-1] = [True] * len(grid[0])
        for y in range(len(grid)):
            grid[y][0] = True
            grid[y][-1] = True
    for y in range(len(grid)):
        for _ in range(n):
            grid[y].insert(0, value)
            grid[y].append(value)
    width = len(grid[0])
    for _ in range(n):
        grid.insert(0, [value] * width)
        grid.append([value] * width)
    return grid

def once(grid: [[bool]], lights: {int}, i: int) -> [[bool]]:
    grid = pad(grid, i % 2 == 1 and 0 in lights, 2)
    #print_grid(grid)
    new_grid = [[False] * len(row) for row in grid]
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
            new_grid[y][x] = get_value(grid, (y, x), lights)
    return new_grid

def cycle(grid: [[bool]], lights: {int}, n: int = 2) -> int:
    for i in range(n):
        grid = once(grid, lights, i)
        #print_grid(grid)
        #print()
    return num_lit(grid)

algorithm, image = open(argv[1]).read().split('\n\n')
grid = make_grid(image.strip().split('\n'))
lights = get_light_locations(''.join(algorithm.strip().split('\n')))
print(cycle(grid, lights))
print(cycle(grid, lights, 50))
