from sys import argv
from math import sqrt

n = int(argv[1])

root = int(sqrt(n))
if root * root != n:
    root += 1
if root % 2 == 0:
    root += 1

def neighbors(grid: [[int]], pos: (int, int)):
    total = 0
    n = len(grid)
    y, x = pos
    left = x > 0
    right = x < n - 1
    up = y > 0
    down = y < n - 1
    if left:
        total += grid[y][x-1]
    if right:
        total += grid[y][x+1]
    if up:
        total += grid[y-1][x]
    if down:
        total += grid[y+1][x]
    if left and up:
        total += grid[y-1][x-1]
    if right and up:
        total += grid[y-1][x+1]
    if left and down:
        total += grid[y+1][x-1]
    if right and down:
        total += grid[y+1][x+1]
    return total

def make_grid(n: int, size: int):
    grid = [[0] * size for _ in range(size)]
    moves = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    def move(pos: (int, int), amt: (int, int)) -> (int, int):
        return (pos[0] + amt[0], pos[1] + amt[1])
    pos = (size//2, size//2)
    grid[pos[0]][pos[1]] = 1
    step = 1
    dir_index = 0
    while True:
        dir = moves[dir_index % len(moves)]
        for _ in range(step):
            pos = move(pos, dir)
            v = neighbors(grid, pos)
            grid[pos[0]][pos[1]] = v
            if v > n:
                #print('\n'.join(' '.join(str(c).rjust(3) for c in row) for row in grid))
                return v
        dir_index += 1
        
        dir = moves[dir_index % len(moves)]
        for _ in range(step):
            pos = move(pos, dir)
            v = neighbors(grid, pos)
            grid[pos[0]][pos[1]] = v
            if v > n:
                #print('\n'.join(' '.join(str(c).rjust(3) for c in row) for row in grid))
                return v
        dir_index += 1

        step += 1

print(make_grid(n, root))
