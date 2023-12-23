from sys import argv
from collections import namedtuple as nt
from itertools import pairwise
from functools import cache

MapEntry = nt('MapEntry', ['dst', 'src', 'len'])

@cache
def map_get(map: (MapEntry), value: int):
    for entry in map:
        if entry.src <= value <= entry.src + entry.len:
            return entry.dst + value - entry.src
    return value

def make_map_entry(line: str) -> MapEntry:
    toks = list(map(int, line.split()))
    return MapEntry(*toks)
        
with open(argv[1]) as fp:
    lines = fp.readlines()

maps = [list() for _ in range(9)]
count = 0
for line in lines:
    line = line.strip()
    if len(line) > 0:
        if line[0].isdigit():
            maps[count].append(make_map_entry(line))
        elif line[0].isalpha():
            if count == 0:
                seeds = list(map(int, line.split(':')[1].strip().split()))
                count += 1
                maps[count] = []
                continue
            maps[count] = tuple(maps[count])
            count += 1
            maps[count] = []
maps.pop(0)
maps.pop(0)
maps[-1] = tuple(maps[-1])
maps = tuple(maps)

@cache
def get_location_from_seed(seed: int) -> int:
    value = seed
    for m in maps:
        value = map_get(m, value)
    return value

answer = min(get_location_from_seed(i) for i in seeds)
print(answer)

seed_ranges = [(seeds[i],seeds[i+1]) for i in range(0, len(seeds), 2)]

def get_location_from_seed_range(start, length):
    print(start, length)
    return min(get_location_from_seed(i) for i in range(start, start + length))

answer = min(get_location_from_seed_range(start, length) for (start, length) in seed_ranges)
print(answer)