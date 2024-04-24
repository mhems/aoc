from sys import argv
from collections import defaultdict
from tqdm import tqdm

def distance(a: (int, int), b: (int, int)) -> int:
    return sum(abs(i - j) for i, j in zip(a, b))

def parse_line(line: str) -> ((int, int), (int, int), int):
    tokens = line.strip().replace(',', '').replace(':', '').split()
    coords = [int(tokens[i].split('=')[1]) for i in (2, 3, 8, 9)]
    return tuple(coords[:2]), tuple(coords[2:])

def get_exclusion_ranges(sensor: (int, int), radius: int, bounds: (int, int)) -> {int: (int, int)}:
    sx, sy = sensor
    lower, upper = bounds
    ranges = dict()
    start = sx - radius + 1
    end = sx + radius - 1
    for dist in range(1, radius + 1):
        r = (max(bounds[0], start), min(bounds[1], end) + 1)
        if lower <= sy - dist <= upper:
            ranges[sy - dist] = r
        if lower <= sy + dist <= upper:
            ranges[sy + dist] = r
        start += 1
        end -= 1
    if lower <= sy <= upper:
        ranges[sy] = max(lower, sx - radius), min(sx + radius, upper) + 1
    return ranges

def consolidate(s: {(int, int)}) -> (int, int):
    ordered = sorted(s)
    itr = iter(ordered)
    start, end = next(itr)
    for s, e in itr:
        if s < start and e >= start:
            start = s
        if e > end and start <= s <= end:
            end = e
    return start, end

def merge_ranges(d1: {int: {(int, int)}}, d2: {int: (int, int)}) -> {int: {(int, int)}}:
    if not d1:
        return {k: {v} for k, v in d2.items()}
    cum = defaultdict(set, d1)
    for y, range in d2.items():
        cum[y].add(range)
    return cum

def get_points_within_on_line(sensor: (int, int), d: int, y: int) -> {(int, int)}:
    sx, sy = sensor
    diff = abs(sy - y)
    new_diff = 2 * (d - diff) + 1
    points = set()
    start = sx - d + diff
    for x in range(start, start + new_diff):
        points.add((x, y))
    return points

def non_beacons_on_line(pairs: ((int, int), (int, int)), Y: int = 2000000) -> int:
    points = set()
    for sensor, beacon in pairs:
        d = distance(sensor, beacon)
        if sensor[1] - d <= Y <= sensor[1] + d:
            points.update(get_points_within_on_line(sensor, d, Y))
    for sensor, beacon in pairs:
        if sensor in points:
            points.remove(sensor)
        if beacon in points:
            points.remove(beacon)
    return len(points)

def build_ranges(pairs: ((int, int), (int, int)), bounds: (int, int) = (0, 4000000)) -> int:
    cum: {int: {(int, int)}} = dict()
    lower, upper = bounds
    for sensor, beacon in tqdm(pairs):
        d = distance(sensor, beacon)
        ranges = get_exclusion_ranges(sensor, d, bounds)
        cum = merge_ranges(cum, ranges)
        
        if lower <= sensor[0] <= upper and lower <= sensor[1] <= upper:
            cum[sensor[1]].add((sensor[0], sensor[0] + 1))
        if lower <= beacon[0] <= upper and lower <= beacon[1] <= upper:
            cum[beacon[1]].add((beacon[0], beacon[0] + 1))
    for y in cum.keys():
        if lower <= y <= upper:
            start, end = consolidate(cum[y])
            if start > bounds[0]:
                return (start - 1) * bounds[1] + y
            if end < bounds[1]:
                return end * bounds[1] + y

pairs = [parse_line(line.strip()) for line in open(argv[1]).readlines()]
print(non_beacons_on_line(pairs))
print(build_ranges(pairs))
