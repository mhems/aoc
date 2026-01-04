from sys import argv
import re
from collections import namedtuple
from itertools import product
from heapq import heappush, heappop

Cube = namedtuple('Cube', ('xmin ymin zmin xmax ymax zmax'))

def distance(pos1: tuple[int, int, int], pos2: tuple[int, int, int]) -> int:
    return sum(abs(a - b) for a, b in zip(pos1, pos2))

def in_range(bot: tuple[int, int, int, int], pos: tuple[int, int, int]) -> bool:
    return distance(bot[:-1], pos) <= bot[-1]

bots = [tuple(map(int, re.findall(r'-?\d+', line.strip()))) for line in open(argv[1]).readlines()]
by_radius = sorted(bots, key=lambda l: l[-1], reverse=True)
centers = [tuple(bot[:-1]) for bot in by_radius]
radii = [bot[-1] for bot in by_radius]
print(1 + sum(int(in_range(by_radius[0], center)) for center in centers[1:]))

cubes = [Cube(x-r, y-r, z-r, x+r, y+r, z+r) for ((x, y, z), r) in zip(centers, radii)]

def super_cube():
    xmin, xmax, ymin, ymax, zmin, zmax = 1e9, 0, 1e9, 0, 1e9, 0
    for cube in cubes:
        xmin = min(xmin, cube.xmin)
        ymin = min(ymin, cube.ymin)
        zmin = min(zmin, cube.zmin)
        xmax = max(xmax, cube.xmax) + 1
        ymax = max(ymax, cube.ymax) + 1
        zmax = max(zmax, cube.zmax) + 1
    return Cube(xmin, ymin, zmin, xmax, ymax, zmax)

def split_cube(cube):
    xs = (cube.xmin, cube.xmin + (cube.xmax - cube.xmin)//2, cube.xmax)
    ys = (cube.ymin, cube.ymin + (cube.ymax - cube.ymin)//2, cube.ymax)
    zs = (cube.zmin, cube.zmin + (cube.zmax - cube.zmin)//2, cube.zmax)
    return [Cube(xmin, ymin, zmin, xmax, ymax, zmax)
            for (xmin, xmax), (ymin, ymax), (zmin, zmax) in
            product(((xs[0], xs[1]), (xs[1], xs[2])),
                    ((ys[0], ys[1]), (ys[1], ys[2])),
                    ((zs[0], zs[1]), (zs[1], zs[2])))]

def bot_in_cube(bot, cube):
    *center, r = bot
    cx, cy, cz = center

    dist = 0
    for c, lo, hi in [(cx,cube.xmin,cube.xmax),(cy,cube.ymin,cube.ymax),(cz,cube.zmin,cube.zmax)]:
        if c < lo:
            dist += lo - c
        elif c > hi:
            dist += c - hi

    return dist <= r

def num_bots_in_range_of_cube(cube):
    return sum(int(bot_in_cube(bot, cube)) for bot in bots)

def num_bots_in_range(point):
    return sum(int(in_range(bot, point)) for bot in bots)

def volume(cube):
    return (cube.xmax-cube.xmin)*(cube.ymax-cube.ymin)*(cube.zmax-cube.zmin)

def center(cube):
    return (cube.xmin + (cube.xmax - cube.xmin)//2,
            cube.ymin + (cube.ymax - cube.ymin)//2,
            cube.zmin + (cube.zmax - cube.zmin)//2)

def search():
    q = []
    heappush(q, (0, super_cube(), len(cubes), 0, 2, 0))
    most = 0
    closest = 1e15
    while q:
        _, cube, num_bots_overlapping, num_in_range, cube_volume, origin_distance = heappop(q)
        if cube_volume <= 1:
            if num_in_range >= most:
                if num_in_range > most:
                    closest = origin_distance
                if origin_distance <= closest:
                    #print('best result', num_in_range, num_bots_overlapping, cube, cube_volume, origin_distance, flush=True)
                    closest = origin_distance
                most = num_in_range
        elif num_bots_overlapping >= most:
            for split in split_cube(cube):
                n = num_bots_in_range_of_cube(split)
                r = num_bots_in_range(center(split))
                v = volume(cube)
                d = distance(center(split), (0, 0, 0))
                heappush(q, ((-n, d, len(str(v))), split, n, r, v, d))
    return closest

print(search())
