from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

def get_extremes(coords: [(int, int)]) -> ((int, int), (int, int)):
    min_x = min(coord[0] for coord in coords)
    max_x = max(coord[0] for coord in coords)
    min_y = min(coord[1] for coord in coords)
    max_y = max(coord[1] for coord in coords)
    return (min_x, max_x), (min_y, max_y)

def distance(pos1: (int, int), pos2: (int, int)) -> int:
    return sum(abs(a - b) for a, b in zip(pos1, pos2))

def distances(pos1: (int, int), coords: [(int, int)]) -> {int: int}:
    '''Return dict mapping coord-index to distance from pos1'''
    return {i: distance(coord, pos1) for i, coord in enumerate(coords)}

def largest_area(coords: [(int, int)], debug=False) -> int:
    (min_x, max_x), (min_y, max_y) = get_extremes(coords)
    grid = [[None] * (max_x) for _ in range(max_y)]
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            d = distances((x, y), coords)
            shortest = min(d.values())
            num = [k for k in d.keys() if d[k] == shortest]
            if len(num) == 1:
                grid[y][x] = num[0]
    if debug:
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if grid[y][x] is None:
                    print('.', end='')
                else:
                    if grid[y][x] < 26:
                        ch = chr(ord('a') + grid[y][x])
                    else:
                        ch = chr(ord('A') + grid[y][x] - 26)
                    print(ch, end='')
            print()
    infinite = set()
    for x in range(min_x, max_x):
        infinite.add(grid[min_y][x])
        infinite.add(grid[max_y-1][x])
    for y in range(min_y, max_y):
        infinite.add(grid[y][min_x])
        infinite.add(grid[y][max_x-1])
    freqs = {}
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            v = grid[y][x]
            if v is not None and v not in infinite:
                if v not in freqs:
                    freqs[v] = 0
                freqs[v] += 1   
    return max(freqs.values())

def epicenter_area(coords: [(int, int)], radius=10_000) -> int:
    (min_x, max_x), (min_y, max_y) = get_extremes(coords)
    area = 0
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            d = sum(distances((x, y), coords).values())
            if d < radius:
                area += 1
    return area 

coords = [tuple(map(int, line.strip().split(', '))) for line in lines]
print(largest_area(coords))
print(epicenter_area(coords))
