from sys import argv
from collections import namedtuple as nt

Pos = nt('Pos', ['x', 'y'])

with open(argv[1]) as fp:
    lines = fp.readlines()

def num_houses(steps: str) -> int:
    houses_seen = set()
    pos = Pos(0, 0)
    houses_seen.add(pos)
    dirs = {'>': Pos(1, 0), '<': Pos(-1, 0), '^': Pos(0, 1), 'v': Pos(0, -1)}
    for dir in steps:
        delta = dirs[dir]
        pos = Pos(pos.x + delta.x, pos.y + delta.y)
        houses_seen.add(pos)
    return len(houses_seen)

def num_houses2(steps: str) -> int:
    houses_seen = set()
    santa_pos = Pos(0, 0)
    robo_pos = Pos(0, 0)
    houses_seen.add(santa_pos)
    dirs = {'>': Pos(1, 0), '<': Pos(-1, 0), '^': Pos(0, 1), 'v': Pos(0, -1)}
    for a, b in zip(steps[::2], steps[1::2]):
        santa_delta, robo_delta = dirs[a], dirs[b]
        santa_pos = Pos(santa_pos.x + santa_delta.x, santa_pos.y + santa_delta.y)
        robo_pos = Pos(robo_pos.x + robo_delta.x, robo_pos.y + robo_delta.y)
        houses_seen.add(santa_pos)
        houses_seen.add(robo_pos)
    return len(houses_seen)

for line in lines:
    print(num_houses(line.strip()))

for line in lines:
    print(num_houses2(line.strip()))