from sys import argv
from tqdm import tqdm
import re

with open(argv[1]) as fp:
    lines = fp.readlines()

regex = re.compile(r'position=< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>')

def parse(line: str) -> ([int, int], (int, int)):
    ints = [int(m) for m in re.match(regex, line.strip()).groups()]
    return [ints[0], ints[1]], (ints[2], ints[3])

def step(stats: ([int, int], (int, int))) -> ([(int, int)], int):
    min_height_diff = 1e6
    min_pos = None
    itr = 0
    while min_height_diff > 12 or itr < 100:
        for i in range(len(stats)):
            stats[i][0][0] += stats[i][1][0]
            stats[i][0][1] += stats[i][1][1]
        ys = [stat[0][1] for stat in stats]
        diff = max(ys) - min(ys)
        if diff < min_height_diff:
            min_height_diff = diff
            min_pos = list(tuple(stat[0]) for stat in stats)
        itr += 1
    return min_pos, itr

def render(positions: [(int, int)]):
    xs = [position[0] for position in positions]
    ys = [position[1] for position in positions]
    min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)
    grid = [[False] * (max_x-min_x+1) for _ in range(max_y-min_y+1)]
    for position in positions:
        grid[position[1] - min_y][position[0] - min_x] = True
    for row in grid:
        for col in row:
            if col:
                print('#', end='')
            else:
                print(' ', end='')
        print()    

stats = [parse(line.strip()) for line in lines]
positions, num = step(stats)
render(positions)
print(num)
