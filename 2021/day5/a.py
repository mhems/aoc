from sys import argv
from collections import defaultdict

def parse_coord(text: str) -> (int, int):
    return tuple(map(int, text.strip().split(',')))

def parse_line(text: str) -> ((int, int), (int, int)):
    return tuple(map(parse_coord, text.strip().split(' -> ')))

def num_overlap(lines: [((int, int), (int, int))], diagonal: bool = False) -> int:
    point_freqs = defaultdict(int)
    for a, b in lines:
        gen = []
        if a[0] == b[0]:
            gen = [(a[0], y) for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1)]
        elif a[1] == b[1]:
            gen = [(x, a[1]) for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1)]
        elif diagonal:
            dx = 1 if a[0] < b[0] else -1
            dy = 1 if a[1] < b[1] else -1
            gen = [(a[0] + dx * i, a[1] + dy * i) for i in range(abs(a[0] - b[0]) + 1)]
        for pair in gen:
            point_freqs[pair] += 1
    return sum(v >= 2 for v in point_freqs.values())

lines = [parse_line(line.strip()) for line in open(argv[1]).readlines()]
print(num_overlap(lines))
print(num_overlap(lines, True))
