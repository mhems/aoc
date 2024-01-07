from sys import argv
from collections import namedtuple as nt

Pos = nt('Pos', ['x', 'y'])
Step = nt('Step', ['func', 'c1', 'c2'])

with open(argv[1]) as fp:
    lines = fp.readlines()

def on(grid: [[bool]], pos: Pos):
    grid[pos.y][pos.x] = True
    
def off(grid: [[bool]], pos: Pos):
    grid[pos.y][pos.x] = False
    
def toggle(grid: [[bool]], pos: Pos):
    grid[pos.y][pos.x] = not grid[pos.y][pos.x]

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

def apply_step(grid: [[bool]], step: Step):
    for x in range(step.c1.x, step.c2.x + 1):
        for y in range(step.c1.y, step.c2.y + 1):
            step.func(grid, Pos(x, y))

def num_lit(grid: [[bool]]) -> int:
    return sum(sum(int(cell) for cell in row) for row in grid)

grid = [[False] * 1000 for _ in range(1000)]
steps = [parse_step(line) for line in lines]

for step in steps:
    apply_step(grid, step)

print(num_lit(grid))
