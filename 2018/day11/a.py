from sys import argv
from tqdm import tqdm

sn = int(argv[1])

def power_level(x: int, y: int, sn: int) -> int:
    rack_id = x + 10
    level = rack_id * y + sn
    level *= rack_id
    hundreds = (level % 1000) // 100
    return hundreds - 5

def make_grid(n: int, sn: int) -> [[int]]:
    grid = [[None] * (n+1) for _ in range(n+1)]
    for y in range(1, n+1):
        for x in range(1, n+1):
            grid[y][x] = power_level(x, y, sn)
    return grid

def find_max_fixed_square(grid: [[int]], n: int, start_x: int = 1, start_y: int = 1) -> (int, (int, int)):
    max_pos = None
    max_level = 0
    for y in range(start_y, len(grid) - n + 1):
        for x in range(start_x, len(grid) - n + 1):
            total = sum(sum(grid[i][x:x+n]) for i in range(y, y+n))
            if total > max_level:
                max_level = total
                max_pos = (x, y)
    return max_level, max_pos

def find_max_variable_square(grid: [[int]]) -> (int, int, int):
    max_pos = None
    max_level = 0
    for y in tqdm(range(1, len(grid))):
        for x in tqdm(range(1, len(grid))):
            for n in tqdm(range(250, len(grid) - max(x, y))):
                level, pos = find_max_fixed_square(grid, n, x, y)
                if level > max_level:
                    max_level = level
                    max_pos = pos, n
    return max_pos

grid = make_grid(300, sn)
print(find_max_fixed_square(grid, 3))
print(find_max_variable_square(grid))
