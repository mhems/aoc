from sys import argv

def num_visible(grid: [[str]]) -> int:
    visible = set()
    W, H = len(grid[0]), len(grid)
    for y in range(H):
        visible.add((y, 0))
        visible.add((y, W - 1))
    for x in range(W):
        visible.add((0, x))
        visible.add((H - 1, x))
    for y in range(1, H-1):
        for x in range(1, W-1):
            if grid[y][x] > max(grid[y][:x]):
                visible.add((y, x))
        for x in range(W-2, 0, -1):
            if grid[y][x] > max(grid[y][x+1:]):
                visible.add((y, x))
    for x in range(1, W-1):
        for y in range(1, H-1):
            if grid[y][x] > max(grid[r][x] for r in range(y)):
                visible.add((y, x))
        for y in range(H-2, 0, -1):
            if grid[y][x] > max(grid[r][x] for r in range(y+1, H)):
                visible.add((y, x))
    return len(visible)

def scenic_score(grid: [[str]], pos: (int, int)) -> int:
    product = 1
    y, x = pos
    t = y - 1
    while t >= 0 and grid[t][x] < grid[y][x]:
        t -= 1
    if t == -1:
        t += 1
    product *= y - t
    t = y + 1
    while t < len(grid) and grid[t][x] < grid[y][x]:
        t += 1
    if t == len(grid):
        t -= 1
    product *= t - y
    t = x - 1
    while t >= 0 and grid[y][t] < grid[y][x]:
        t -= 1
    if t == -1:
        t += 1
    product *= x - t
    t = x + 1
    while t < len(grid[0]) and grid[y][t] < grid[y][x]:
        t += 1
    if t == len(grid[0]):
        t -= 1
    product *= t - x
    return product

def max_scenic_score(grid: [[str]]) -> int:
    return max(max(scenic_score(grid, (y, x)) for x in range(len(grid[0]))) for y in range(len(grid)))

grid = [list(map(int, line.strip())) for line in open(argv[1]).readlines()]
print(num_visible(grid))
print(max_scenic_score(grid))
