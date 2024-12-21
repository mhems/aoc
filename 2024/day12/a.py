from sys import argv
from collections import deque

def neighbors(pos: (int, int), Y: int = None, X: int = None) -> [(int, int)]:
    deltas = [(-1, 0), (0, -1), (0, 1), (1, 0)]
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
                for plant in region:
                    visited.add(plant)
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

def num_sides(region: {(int, int)}) -> int:
    if len(region) < 3:
        return 4
    # num turns + 1
    print(region)
    top_left = min(region)
    xs = {x for _, x in region}
    ys = {y for y, _ in region}
    minX, maxX = min(xs) - 1, max(xs) + 1
    minY, maxY = min(ys) - 1, max(ys) + 1
    exterior = set()
    grid = []
    for _ in range(maxY - minY + 1):
        grid.append([False] * (maxX - minX + 1))
    for y, x in region:
        grid[y-minY][x-minX] = True
    print_grid(grid)
    return 4

def price(region: {(int, int)}) -> int:
    return area(region) * perimeter(region)

def bulk_price(region: {(int, int)}) -> int:
    return area(region) * num_sides(region)

garden = [list(line.strip()) for line in open(argv[1]).readlines()]
regions = flood_fills(garden)
print(sum(map(price, regions)))
print(sum(map(bulk_price, regions)))
