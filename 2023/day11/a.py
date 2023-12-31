from sys import argv
from collections import namedtuple as nt
from itertools import groupby, pairwise, combinations

Pos = nt('Pos', ['x', 'y'])
Galaxy = nt('Galaxy', ['num', 'pos'])

with open(argv[1]) as fp:
    lines = fp.readlines()

galaxies = set()
for row, line in enumerate(lines):
    for col, char in enumerate(line.strip()):
        if char == '#':
            galaxies.add(Galaxy(len(galaxies)+1, Pos(col, row)))

R = row + 1
C = col + 1
#print(R, 'x', C)
#print('G', len(galaxies))

def get_missing(elements: [int]) -> [int]:
    missing = []
    for a, b in pairwise(elements):
        diff = b - a
        if diff > 0:
            for i in range(a+1, b, 1):
                missing.append(i)
    return missing

def expand_vert(galaxies: {Galaxy}, delta: int = 1) -> {Galaxy}:
    vert_map = {k:list(g)
                for k, g in groupby(sorted(galaxies, key=lambda g: (g.pos.y, g.pos.x)),
                                    key=lambda g: g.pos.y)}
    ys = sorted(set(g.pos.y for g in galaxies))
    missing_ys = get_missing(ys)
    for ym in reversed(missing_ys):
        for yi in range(ym + 1, R):
            if yi in vert_map:
                vert_map[yi] = [Galaxy(g.num, Pos(g.pos.x, g.pos.y + delta)) for g in vert_map[yi]]
    new_gs = set()
    for gs in vert_map.values():
        for g in gs:
            new_gs.add(g)
    return len(missing_ys)  * delta, new_gs

def expand_horz(galaxies: {Galaxy}, delta: int = 1) -> {Galaxy}:
    horz_map = {k:list(g)
                for k, g in groupby(sorted(galaxies, key=lambda g: (g.pos.x, g.pos.y)),
                                    key=lambda g: g.pos.x)}
    xs = sorted(set(g.pos.x for g in galaxies))
    missing_xs = get_missing(xs)
    for xm in reversed(missing_xs):
        for xi in range(xm + 1, C):
            if xi in horz_map:
                horz_map[xi] = [Galaxy(g.num, Pos(g.pos.x + delta, g.pos.y)) for g in horz_map[xi]]
    new_gs = set()
    for gs in horz_map.values():
        for g in gs:
            new_gs.add(g)
    return len(missing_xs) * delta, new_gs

def print_galaxies(galaxies: {Galaxy}):
    for r in range(R + dy):
        for c in range(C + dx):
            if any(g.pos == Pos(c, r) for g in galaxies):
                print('#', end='')
            else:
                print('.', end='')
        print()

def shortest_path(p1: Pos, p2: Pos) -> int:
    return abs(p2.y - p1.y) + abs(p2.x - p1.x)

# print_galaxies(galaxies)
dy, expanded_galaxies = expand_vert(galaxies)
dx, expanded_galaxies = expand_horz(expanded_galaxies)
#print('dx', dx)
#print('dy', dy)
# print_galaxies(expanded_galaxies)
combos = combinations(expanded_galaxies, 2)
answer = sum(shortest_path(g1.pos, g2.pos) for g1, g2 in combos)
print(answer)

#print_galaxies(galaxies)
dy, expanded_galaxies = expand_vert(galaxies, 999_999)
dx, expanded_galaxies = expand_horz(expanded_galaxies, 999_999)
#print('dx', dx)
#print('dy', dy)
#print_galaxies(expanded_galaxies)
combos = combinations(expanded_galaxies, 2)
answer = sum(shortest_path(g1.pos, g2.pos) for g1, g2 in combos)
print(answer)