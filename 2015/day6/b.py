from sys import argv
from collections import namedtuple as nt

Pos = nt('Pos', ['x', 'y'])
Step = nt('Step', ['func', 'c1', 'c2'])

with open(argv[1]) as fp:
    lines = fp.readlines()

def on(grid: [[int]], pos: Pos):
    grid[pos.y][pos.x] += 1
    
def off(grid: [[int]], pos: Pos):
    if grid[pos.y][pos.x] > 0:
        grid[pos.y][pos.x] -= 1
    
def toggle(grid: [[int]], pos: Pos):
    grid[pos.y][pos.x] += 2

def parse_pos(text: str) -> Pos:
    return Pos(*map(int, text.split(',')))

def parse_step(line: str) -> Step:
    tokens = line.strip().split()
    if tokens[0] == 'turn':
        func = on if tokens[1] == 'on' else off
        c1 = parse_pos(tokens[2])
        c2 = parse_pos(tokens[4])
    else:
        func = toggle
        c1 = parse_pos(tokens[1])
        c2 = parse_pos(tokens[3])
    return Step(func, c1, c2)

def apply_step(grid: [[int]], step: Step):
    for x in range(step.c1.x, step.c2.x + 1):
        for y in range(step.c1.y, step.c2.y + 1):
            step.func(grid, Pos(x, y))

def brightness(grid: [[int]]) -> int:
    return sum(sum(cell for cell in row) for row in grid)

grid = [[0] * 1000 for _ in range(1000)]
steps = [parse_step(line) for line in lines]

for step in steps:
    apply_step(grid, step)

print(brightness(grid))
