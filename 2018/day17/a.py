from sys import argv
import re

regex = re.compile(r'.=(\d+), .=(\d+)\.\.(\d+)')
minY, maxY = 0, 0

def make_grid(lines: [str]) -> [[str]]:
    global minY, maxY
    walls = []
    for line in lines:
        vert = line.startswith('x')
        nums = [int(group) for group in re.match(regex, line.strip()).groups()]
        if vert:
            walls.extend((n, nums[0]) for n in range(nums[1], nums[2] + 1))
        else:
            walls.extend((nums[0], n) for n in range(nums[1], nums[2] + 1))
    xs, ys = [x for _, x in walls], [y for y, _ in walls]
    X, Y = max(xs) + 2, max(ys) + 2
    minY, maxY = min(ys), max(ys)
    grid = [['.'] * X for _ in range(Y)]
    for y, x in walls:
        grid[y][x] = '#'
    return grid

def print_grid(grid: [[str]], spout: int = None):
    if spout:
        print(' ' * spout + 'V')
    for row in grid:
        for cell in row:
            print(cell, end='')
        print()
    print()

def get(pos: (int, int), grid: [[str]]):
    return grid[pos[0]][pos[1]]

def set(pos: (int, int), value: str, grid: [[str]]):
    if clay(pos, grid):
        raise ValueError(pos)
    grid[pos[0]][pos[1]] = value

def drip(pos: (int, int), grid: [[str]]):
    set(pos, '|', grid)
    
def water(pos: (int, int), grid: [[str]]):
    set(pos, '~', grid)

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

def surface(pos: (int, int), grid: [[str]]) -> bool:
    return get(pos, grid) in ('~', '#')

def num_wet(grid: [[str]], include_falling=True) -> int:
    total = 0
    for i, row in enumerate(grid):
        if minY <= i <= maxY:
            for line in row:
                total += line.count('~')
                if include_falling:
                    total += line.count('|')
    return total

def trace_down(spout: (int, int), grid: [[str]]):
    pos = spout

    if pos[0] < 0 or pos[0] >= len(grid) or pos[1] < 0 or pos[1] >= len(grid[0]):
        return
    while pos[0] < len(grid) and not surface(pos, grid):
        drip(pos, grid)
        pos = down(pos)
    if pos[0] == len(grid):
        return
    hit = pos
    # go up while we have clay on both sides
    bound = True
    while bound:
        bound = False
        hit = up(hit)
        pos = hit
        # go left until we hit clay or lose our surface
        while pos[1] >= 0 and surface(down(left(pos)), grid) and not clay(left(pos), grid):
            pos = left(pos)
        left_start = pos
        left_is_clay = clay(left(left_start), grid)

        pos = hit
        # go right until we hit clay or lose our surface
        while pos[1] < len(grid[0]) - 1 and surface(down(right(pos)), grid) and not clay(right(pos), grid):
            pos = right(pos)
        right_end = pos

        if left_is_clay:
            if clay(right(pos), grid):
                bound = True
                for i in range(left_start[1], right_end[1] + 1):
                    water((right_end[0], i), grid)
            else:
                right_end = pos
                for i in range(left_start[1], right_end[1] + 1):
                    set((right_end[0], i), '|', grid) # $
                    
                right_corner = right((pos[0], right_end[1]))
                if sand(right_corner, grid):
                   drip(right_corner, grid)
                   trace_down(right_corner, grid)

    for i in range(left_start[1], right_end[1] + 1):
        set((pos[0], i), '|', grid) # !
    left_corner = left((pos[0], left_start[1]))
    if sand(left_corner, grid):
        drip(left_corner, grid)
        trace_down(left_corner, grid)
    
    right_corner = (pos[0], right_end[1])
    if (right_corner[1] < len(grid[0]) - 1 and sand(right(right_corner), grid)):
        right_corner = right(right_corner)
        if sand(right_corner, grid):
            set(right_corner, '|', grid) # @
            trace_down(right_corner, grid)

def replace_enclosed(grid: [[str]]):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '|' and grid[y-1][x] == '~':
                grid[y][x] = '~'

with open(argv[1]) as fp:
    lines = fp.readlines()

grid = make_grid(lines)
trace_down((0, 500), grid)
replace_enclosed(grid)
#print_grid(grid, spout)
print(num_wet(grid))
print(num_wet(grid, False))
