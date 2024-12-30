from sys import argv
from collections import deque
from PIL import Image
from random import randint

def neighbors(pos: (int, int), Y: int = None, X: int = None) -> [(int, int)]:
    deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    return [(pos[0] + dy, pos[1] + dx) for dy, dx in deltas
            if (Y is None or 0 <= pos[0] + dy < Y) and (X is None or 0 <= pos[1] + dx < X)]

def flood(garden: [[str]], start: (int, int)) -> {(int, int)}:
    plant = garden[start[0]][start[1]]
    q = deque([start])
    Y, X = len(garden), len(garden[0])
    visited = set()
    visited.add(start)
    while q:
        pos = q.popleft()
        for n in neighbors(pos, Y, X):
            if n not in visited and plant == garden[n[0]][n[1]]:
                visited.add(n)
                q.append(n)
    return visited

def flood_fills(garden: [[str]]) -> [{(int, int)}]:
    regions = []
    visited = set()
    for y, row in enumerate(garden):
        for x, _ in enumerate(row):
            if (y, x) not in visited:
                region = flood(garden, (y, x))
                visited.update(region)
                regions.append(region)
    return regions

def area(region: {(int, int)}) -> int:
    return len(region)

def perimeter(region: {(int, int)}) -> int:
    return sum(sum(int(pos not in region) for pos in neighbors(plant)) for plant in region)

def print_grid(grid: [[bool]]):
    for row in grid:
        for cell in row:
            print('#' if cell else '.', end='')
        print()

def num_corners(region: {(int, int)}) -> int:
    num = 0
    for y, x in region:
        for dy in (-1, 1):
            for dx in (-1, 1):
                p1_in = (y+dy, x) in region
                p2_in = (y, x+dx) in region
                if not p1_in and not p2_in:
                    num += 1
                elif p1_in and p2_in and (y+dy, x+dx) not in region:
                    num += 1
    return num

def price(region: {(int, int)}) -> int:
    return area(region) * perimeter(region)

def bulk_price(region: {(int, int)}) -> int:
    return area(region) * num_corners(region)

def draw(regions: [{(int, int)}], Y: int, X: int):
    image = Image.new('RGB', (X, Y))
    for region in regions:
        color = randint(0, 255), randint(0, 255), randint(0, 255)
        for pos in region:
            image.putpixel(pos, color)
    image.save('garden.png')

garden = [list(line.strip()) for line in open(argv[1]).readlines()]
regions = flood_fills(garden)
draw(regions, len(garden), len(garden[0]))
print(sum(map(price, regions)))
print(sum(map(bulk_price, regions)))
