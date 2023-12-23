from sys import argv
from collections import namedtuple as nt

MapEntry = nt('MapEntry', ['dst', 'src', 'len'])

def map_get(map: {int:int}, value: int):
    return map.get(value, value)

def make_map_entry(line: str) -> MapEntry:
    toks = list(map(int, line.split()))
    return MapEntry(*toks)

def add_entry(m: {int:int}, line: str):
    entry = make_map_entry(line)
    for i in range(entry.len):
        m[entry.src + i] = entry.dst + i
        
with open(argv[1]) as fp:
    lines = fp.readlines()

maps = [dict() for _ in range(9)]
count = 0
for line in lines:
    line = line.strip()
    if len(line) > 0:
        if line[0].isdigit():
            add_entry(maps[count], line)
        elif line[0].isalpha():
            if count == 0:
                seeds = list(map(int, line.split(':')[1].strip().split()))
            count += 1
            print(count)
maps.pop(0)
maps.pop(0)

def get_location_from_seed(seed: int) -> int:
    value = seed
    for m in maps:
        value = map_get(m, value)
    return value

print(seeds)
answer = min(get_location_from_seed(i) for i in seeds)
print(answer)
