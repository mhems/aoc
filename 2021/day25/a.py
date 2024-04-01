from sys import argv

def once(grid: [[str]]) -> [[str]]:
    moved = False
    new_grid = [list(row) for row in grid]
    for y in range(len(grid)):
        x = 0
        while x < len(grid[0]):
            if grid[y][x] == '>' and grid[y][(x + 1) % len(grid[0])] == '.':
                new_grid[y][x], new_grid[y][(x + 1) % len(grid[0])] = '.', '>'
                moved = True
                x += 1
            x += 1
    grid = new_grid
    new_grid = [list(row) for row in grid]
    for x in range(len(grid[0])):
        y = 0
        while y < len(grid):
            if grid[y][x] == 'v' and grid[(y + 1) % len(grid)][x] == '.':
                new_grid[y][x], new_grid[(y + 1) % len(grid)][x] = '.', 'v'
                moved = True
                y += 1
            y += 1
    return new_grid, moved

def until_stop(grid: [[str]]) -> int:
    i = 0
    while True:
        grid, moved = once(grid)
        i += 1
        if not moved:
            return i

grid = [list(line.strip()) for line in open(argv[1]).readlines()]
print(until_stop(grid))