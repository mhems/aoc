import sys

def num_adjacent(grid: list[list[str]], y: int, x: int) -> int:
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return sum(int(grid[dy+y][dx+x] == '@') for dy, dx in deltas)

grid = [['.'] + list(line.strip()) + ['.'] for line in open(sys.argv[1]).readlines()]
grid.insert(0, ['.'] * len(grid[0]))
grid.append(['.'] * len(grid[0]))

def remove(grid: list[list[str]]) -> int:
    accessible = []
    for y in range(1, len(grid)-1):
        for x in range(1, len(grid[0])-1):
            if grid[y][x] == '@' and num_adjacent(grid, y, x) < 4:
                accessible.append((y, x))
    for y, x in accessible:
        grid[y][x] = 'x'
    return len(accessible)

part1 = remove(grid)
print(part1)

def remove_all(grid: list[list[str]]) -> int:
    total = 0
    while True:
        num_changed = remove(grid)
        total += num_changed
        if num_changed == 0:
            return total

print(part1 + remove_all(grid))
