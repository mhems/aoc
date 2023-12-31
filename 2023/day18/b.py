from sys import argv
from collections import namedtuple as nt
from itertools import groupby, pairwise
from bisect import bisect_left

Pos = nt('Pos', ['x', 'y'])
Step = nt('Step', ['dir', 'num', 'color'])
Wall = nt('Wall', ['pos', 'color'])

def parse_step_a(s: str) -> Step:
    tokens = s.strip().split()
    color = tokens[2].strip('()')[1:]
    dir = tokens[0]
    return Step(dir, int(tokens[1]), dir)

def parse_step(s: str) -> Step:
    tokens = s.strip().split()
    color = tokens[2].strip('()')[1:]
    dir = 'RDLU'[int(color[5])]
    return Step(dir, int(color[:5], 16), dir)

with open(argv[1]) as fp:
    lines = fp.readlines()
steps = list(map(parse_step, lines))
#print('\n'.join(map(str, steps)))

walls = []
cur = Pos(0, 0)
for s, step in enumerate(steps):
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
    if step.dir in 'LR':
        walls[-1] = Wall(walls[-1].pos, steps[s+1].color)
    cur = walls[-1].pos

perimeter = len(walls)
print('perimeter', perimeter)
#R = max(wall.pos.y for wall in walls) - min(wall.pos.y for wall in walls) + 1
#C = max(wall.pos.x for wall in walls) - min(wall.pos.x for wall in walls) + 1
#print('dims', R, C)
sorted_walls = sorted(walls, key=lambda wall: (wall.pos.y, wall.pos.x))
grouped_walls = {k: list(g)
                 for k, g in groupby(sorted_walls, key=lambda wall: wall.pos.y)}
debug_perimeter = False

if debug_perimeter:
    for y, walls in grouped_walls.items():
        print('%4d' % y, end=" ")
        for c in range(C):
            key = Pos(c, y)
            index = bisect_left(walls, key, key=lambda wall: wall.pos)
            if index != len(walls) and walls[index].pos == key:
                print('>V<^'['RDLU'.index(walls[index].color)], end='')
            else:
                print('.', end='')
        print()

def get_inner_area(wall_groups: {int: [Wall]}) -> int:
    count = 0
    for y, walls in wall_groups.items():
        i = 0
        N = len(walls)
        while i < N-1:
            if walls[i].pos.x + 1 == walls[i+1].pos.x:
                i += 1
                continue
            if walls[i].color == 'U' and walls[i+1].color == 'D':
                add = walls[i+1].pos.x - walls[i].pos.x - 1
                count += add
                i += 2
            else:
                i += 1
    return count

inner_count = get_inner_area(grouped_walls)
print('inner', inner_count)
print('total', perimeter + inner_count)