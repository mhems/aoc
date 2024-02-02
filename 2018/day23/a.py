from sys import argv
import re

regex = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')
with open(argv[1]) as fp:
    lines = fp.readlines()

def parse(line: str) -> [int]:
    return list(map(int, re.match(regex, line.strip()).groups()))

def distance(pos1: [int], pos2: [int]) -> int:
    return sum(abs(a - b) for a, b in zip(pos1, pos2))

bots = [parse(line.strip()) for line in lines]
by_radius = sorted(bots, key=lambda l: l[-1], reverse=True)
strongest = by_radius[0]
in_range = 1 + sum(int(distance(strongest[:-1], other[:-1]) <= strongest[-1]) for other in by_radius[1:])
print(in_range)
