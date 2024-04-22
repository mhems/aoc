from sys import argv

def distance(a: (int, int), b: (int, int)) -> int:
    return sum(abs(i - j) for i, j in zip(a, b))

def parse_line(line: str) -> ((int, int), (int, int), int):
    tokens = line.strip().replace(',', '').replace(':', '').split()
    coords = [int(tokens[i].split('=')[1]) for i in (2, 3, 8, 9)]
    return tuple(coords[:2]), tuple(coords[2:])

def get_points_within(p: (int, int), d: int) -> {(int, int)}:
    points = set()
    sx, sy = p
    for d in range(d, -1, -1):
        for dx, dy in zip(range(d + 1), range(d, -1, -1)):
            points.add((sx + dx, sy + dy))
            points.add((sx - dx, sy + dy))
            points.add((sx + dx, sy - dy))
            points.add((sx - dx, sy - dy))
    return points

def get_points_within_on_line(p: (int, int), d: int, y: int) -> {(int, int)}:
    sx, sy = p
    diff = abs(sy - y)
    new_diff = 2 * (d - diff) + 1
    points = set()
    start = sx - d + diff
    print(new_diff)
    for x in range(start, start + new_diff):
        points.add((x, y))
    return points

def make_grid(pairs: ((int, int), (int, int)), Y: int = 2000000) -> {(int, int): str}:
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

pairs = [parse_line(line.strip()) for line in open(argv[1]).readlines()]
print(make_grid(pairs))
