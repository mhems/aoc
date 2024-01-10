from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()
num_steps = int(argv[2])

grid = [[False] + [l == '#' for l in line.strip()] + [False] for line in lines]
grid.insert(0, [False] * len(grid[0]))
grid.append([False] * len(grid[0]))

def get_value(grid: [[bool]], i: int, j: int, fix: bool = False) -> bool:
    if (fix and
        ((i == 1 and (j == 1 or j == len(grid) - 2)) or
         (i == len(grid) - 2 and (j == 1 or j == len(grid)-2)))):
        return True
    neighbor_locs = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    num_neighbors_on = sum(int(grid[pos[0] + i][pos[1] + j]) for pos in neighbor_locs)
    state = grid[i][j]
    if state:
        return num_neighbors_on == 2 or num_neighbors_on == 3
    return num_neighbors_on == 3

def cycle(grid: [[bool]], fix: bool = False) -> [[bool]]:
    n = len(grid)
    new_grid = [[False]*n for _ in range(n)]
    for i in range(1, n-1):
        for j in range(1, n-1):
            new_grid[i][j] = get_value(grid, i, j, fix)
    return new_grid

def simulate(grid: [[bool]], num_steps: int, fix: bool = False) -> int:
    for _ in range(num_steps):
        grid = cycle(grid, fix)
    return sum(sum(int(cell) for cell in row) for row in grid)

print(simulate(grid, num_steps))
grid[1][1] = True
grid[1][len(grid)-2] = True
grid[len(grid)-2][1] = True
grid[len(grid)-2][len(grid)-2] = True
print(simulate(grid, num_steps, True))