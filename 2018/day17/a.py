from sys import argv
import re

regex = re.compile(r'.=(\d+), .=(\d+)\.\.(\d+)')

def make_grid(lines: [str], limit=None) -> [[str]]:
    walls = []
    for line in lines:
        vert = line.startswith('x')
        nums = [int(group) for group in re.match(regex, line.strip()).groups()]
        if vert:
            walls.extend((n, nums[0]) for n in range(nums[1], nums[2] + 1))
        else:
            walls.extend((nums[0], n) for n in range(nums[1], nums[2] + 1))
    if limit is not None:
        walls = [wall for wall in walls if wall[0] < limit]
    xs, ys = [x for _, x in walls], [y for y, _ in walls]
    minX, minY = min(xs), min(ys)
    X, Y = max(xs) - minX + 1, max(ys) - minY + 1
    grid = [['.'] * X for _ in range(Y)]
    for y, x in walls:
        grid[y-minY][x-minX] = '#'
    return grid, 500 - minX

def print_grid(grid: [[str]], spout: int = None):
    if spout:
        print(' ' * spout + 'V')
    for row in grid:
        for cell in row:
            print(cell, end='')
        print()
    print()
    print('=' * 250)
    print('=' * 250)
    print()

def get(pos: (int, int), grid: [[str]]):
    return grid[pos[0]][pos[1]]

def set(pos: (int, int), value: str, grid: [[str]]):
    grid[pos[0]][pos[1]] = value

def fill(pos: (int, int), grid: [[str]]):
    if clay(pos, grid):
        print_grid(grid)
        raise ValueError(pos)
    set(pos, '|', grid)

def up(pos: (int, int)) -> (int, int):
    return pos[0] - 1, pos[1]

def down(pos: (int, int)) -> (int, int):
    return pos[0] + 1, pos[1]

def left(pos: (int, int)) -> (int, int):
    return pos[0], pos[1] - 1

def right(pos: (int, int)) -> (int, int):
    return pos[0], pos[1] + 1

def clay(pos: (int, int), grid: [[str]]) -> bool:
    return get(pos, grid) == '#'

def sand(pos: (int, int), grid: [[str]]) -> bool:
    return get(pos, grid) == '.'

def trace_down(spout: (int, int), grid: [[str]]):
    pos = spout
    #print_grid(grid)
    #print('start', pos)
    if pos[0] < 0 or pos[0] >= len(grid) or pos[1] < 0 or pos[1] >= len(grid[0]):
        return
    while pos[0] < len(grid) and not clay(pos, grid):
        fill(pos, grid)
        pos = down(pos)
        #print('going down', pos)
    if pos[0] == len(grid):
        return
    pos = up(pos)
    
    hit = pos

    # go left until we hit clay
    while pos[1] >= 0 and clay(down(left(pos)), grid) and not clay(left(pos), grid):
        fill(pos, grid)
        pos = left(pos)
    if clay(left(pos), grid):
        # then go up while clay is on our left
        while pos[0] >= 0 and clay(left(pos), grid):
            fill(pos, grid)
            pos = up(pos)
        if pos[0] < 0:
            return
        fill(pos, grid)
        pos = left(pos)
        fill(pos, grid)
    # and recurse
    if pos[1] > 0:
        trace_down(left(pos), grid)
        #trace_down(pos, grid)
    
    pos = hit
    # go right until we hit clay
    while pos[1] < len(grid[0]) and clay(down(right(pos)), grid) and not clay(right(pos), grid):
        fill(pos, grid)
        pos = right(pos)
    if clay(right(pos), grid):
        # then go up while clay is on our right
        while pos[0] >= 0 and clay(right(pos), grid):
            fill(pos, grid)
            pos = up(pos)
        if pos[0] < 0:
            return
        fill(pos, grid)
        pos = right(pos)
        fill(pos, grid)
    # and recurse
    if pos[1] < len(grid[0]) - 1:
        trace_down(right(pos), grid)
        #trace_down(pos, grid)

with open(argv[1]) as fp:
    lines = fp.readlines()


grid, spout = make_grid(lines, 150)
#print_grid(grid, spout)

try:
    trace_down((0, spout), grid)
except ValueError as e:
    raise e
except:
    pass
print_grid(grid, spout)