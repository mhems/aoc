from sys import argv
import numpy as np

def neighbors2d(grid, pos: (int, int), include_origin: bool) -> int:
    y, x = pos
    return int(sum(grid[y + dy, x + dx]
                   for dy, dx in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1,))
                   if (dy, dx) != (0, 0) or include_origin))

def neighbors3d(grid, pos) -> int:
    z, y, x = pos
    return neighbors2d(grid[z-1], (y, x), True) + neighbors2d(grid[z], (y, x), False) + neighbors2d(grid[z+1], (y, x), True)

def conway(grid, n):
    for _ in range(n):
        todo = []
        for z in range(10, 80):
            for y in range(10, 80):
                for x in range(10, 80):
                    num_active = neighbors3d(grid, (z, y, x))
                    if grid[z, y, x] == 1:
                        if num_active != 2 and num_active != 3:
                            todo.append(((z, y, x), 0))
                    else:
                        if num_active == 3:
                            todo.append(((z, y, x), 1))
        for (z, y, x), v in todo:
            grid[z, y, x] = v

def num_on(grid) -> int:
    count = 0
    for z in range(10, 80):
        for y in range(10, 80):
            for x in range(10, 80):
                if grid[z, y, x]:
                    count += 1
    return int(count)

grid = np.zeros((100, 100, 100), dtype=np.uint8)
for y, row in enumerate(open(argv[1]).readlines()):
    for x, cell in enumerate(row.strip()):
        if cell == '#':
            grid[50, y + 50, x + 50] = 1
conway(grid, 6)
print(num_on(grid))
