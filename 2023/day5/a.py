from sys import argv
from collections import namedtuple as nt

MapEntry = nt('MapEntry', ['dst', 'src', 'len'])
Range = nt('Range', ['start', 'stop'])

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
            count += 1
            maps[count] = []
maps.pop(0)
maps.pop(0)

def get_location_from_seed(seed: int) -> int:
    value = seed
    for m in maps:
        value = map_get(m, value)
    return value

answer = min(get_location_from_seed(i) for i in seeds)
print(answer)

seed_ranges = [Range(seeds[i],seeds[i]+seeds[i+1]) for i in range(0, len(seeds), 2)]

# adapted from https://www.reddit.com/r/adventofcode/comments/18b4b0r/2023_day_5_solutions/
def translate_ranges(entries: [MapEntry], ranges: [Range]) -> [Range]:
    translated_ranges = []
    for entry in entries:
        not_translated_ranges = []
        while ranges:
                cur = ranges.pop()
                before = Range(cur.start, min(cur.stop, entry.src))
                if before[1] > before[0]:
                    not_translated_ranges.append(before)

                overlap = Range(max(cur.start, entry.src), min(cur.stop, entry.src + entry.len))
                if overlap[1] > overlap[0]:
                    # only have to translate the range that overlaps with map entry
                    delta = entry.dst - entry.src
                    translated_ranges.append(Range(overlap[0] + delta, overlap[1] + delta))

                after = Range(max(cur.start, entry.src + entry.len), cur.stop)
                if after[1] > after[0]:
                    not_translated_ranges.append(after)
        ranges = not_translated_ranges
    return translated_ranges + ranges

starts = []
for start, stop in seed_ranges:
    ranges = [Range(start, stop)]
    for m in maps:
        ranges = translate_ranges(m, ranges)
    starts.append(min(r.start for r in ranges))
print(min(starts))