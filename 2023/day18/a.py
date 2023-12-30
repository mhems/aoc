from sys import argv, setrecursionlimit
from collections import namedtuple as nt
from itertools import groupby
from datetime import datetime as dt
from pprint import pprint

setrecursionlimit(10000000)

Pos = nt('Pos', ['x', 'y'])
Step = nt('Step', ['dir', 'num', 'color'])
Wall = nt('Wall', ['pos', 'color'])

def parse_step(s: str) -> Step:
    tokens = s.strip().split()
    num = int(tokens[1])
    color = tokens[2].strip('()')[1:]
    return Step(tokens[0], num, color)

with open(argv[1]) as fp:
    lines = fp.readlines()
steps = list(map(parse_step, lines))
walls = []
cur = Pos(0, 0)
for step in steps:
    if step.dir == 'U':
        for i in range(step.num):
            walls.append(Wall(Pos(cur.x, cur.y - 1 - i), step.color))
    elif step.dir == 'D':
        for i in range(step.num):
            walls.append(Wall(Pos(cur.x, cur.y + 1 + i), step.color))
    elif step.dir == 'L':
        for i in range(step.num):
            walls.append(Wall(Pos(cur.x - 1 - i, cur.y), step.color))
    elif step.dir == 'R':
        for i in range(step.num):
            walls.append(Wall(Pos(cur.x + 1 + i, cur.y), step.color))
    cur = walls[-1].pos

perimeter = len(walls)
print('perimeter', perimeter)
R = max(wall.pos.y for wall in walls) - min(wall.pos.y for wall in walls) + 1
C = max(wall.pos.x for wall in walls) - min(wall.pos.x for wall in walls) + 1

sorted_walls = sorted(walls, key=lambda wall: (wall.pos.y, wall.pos.x))
grouped_walls = [sorted(g, key=lambda wall: wall.pos.x)
                 for _, g in groupby(sorted_walls, key=lambda wall: wall.pos.y)]
#pprint(grouped_walls)
debug_perimeter = False

if debug_perimeter:
    for i, walls in enumerate(grouped_walls):
        print('%4d' % walls[0].pos.y, end=" ")
        for c in range(C):
            if any(wall.pos.x == c for wall in walls):
                print('#', end='')
            else:
                print('.', end='')
        print()

def find_top_left_corner() -> Pos:
    next_row = grouped_walls[1]
    for wall in grouped_walls[0]:
        for below_wall in next_row:
            if below_wall.pos.x == wall.pos.x:
                return Pos(wall.pos.x + 1, wall.pos.y + 1)

def is_wall(pos: Pos) -> bool:
    return any(wall.pos.x == pos.x for wall in grouped_walls[pos.y])

def flood_fill(block: Pos, inner_blocks: [Pos]):
    if block in inner_blocks:
        return
    if not is_wall(block):
        inner_blocks.append(block)
    up = Pos(block.x, block.y - 1)
    if not is_wall(up):
        flood_fill(up, inner_blocks)
    down = Pos(block.x, block.y + 1)
    if not is_wall(down):
        flood_fill(down, inner_blocks)
    left = Pos(block.x - 1, block.y)
    if not is_wall(left):
        flood_fill(left, inner_blocks)
    right = Pos(block.x + 1, block.y)
    if not is_wall(right):
        flood_fill(right, inner_blocks)

corner = find_top_left_corner()
print('corner', corner)
inner_blocks = []
try:
    start = dt.now()
    flood_fill(corner, inner_blocks)
    end = dt.now()
    print(end, start)
    print((end - start).total_seconds())
except RecursionError:
    print('error', len(inner_blocks))

debug_inner = False

if debug_inner:
    for i, walls in enumerate(grouped_walls):
        print('%4d' % walls[0].pos.y, end=" ")
        for c in range(C):
            if any(wall.pos.x == c for wall in walls):
                print('#', end='')
            elif any(block.x == c and block.y == walls[0].pos.y for block in inner_blocks):
                print('*', end='')
            else:
                print('.', end='')
        print()

print('inner', len(inner_blocks))
print('total', perimeter + len(inner_blocks))