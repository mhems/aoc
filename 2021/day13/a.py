from sys import argv

def build_grid(dots: [(int, int)]) -> [[bool]]:
    width = max(x for x, _ in dots) + 1
    height = max(y for _, y in dots) + 1
    grid = [[False] * width for _ in range(height)]
    for x, y in dots:
        grid[y][x] = True
    return grid

def print_grid(grid: [[bool]]):
    for row in grid:
        for cell in row:
            print('#' if cell else '.', end='')
        print()
    print()

def fold_vert(grid: [[bool]], row: int) -> [[bool]]:
    while len(grid)//2 != row:
        grid.append([False] * len(grid[0]))
        grid.append([False] * len(grid[0]))
    height = len(grid)
    assert row == height//2
    new_grid = [[False] * len(grid[0]) for _ in range(height//2)]
    for new_row, (row1, row2) in enumerate(zip(grid[:row], reversed(grid[row+1:]))):
        for c, (c1, c2) in enumerate(zip(row1, row2)):
            new_grid[new_row][c] = c1 or c2
    return new_grid

def fold_horz(grid: [[bool]], col: int) -> [[bool]]:
    width = len(grid[0])
    assert col == width//2
    new_grid = [[False] * (width//2) for _ in range(len(grid))]
    for row in range(len(grid)):
        for i in range(col):
            new_grid[row][i] = grid[row][i] or grid[row][width - 1 - i]
    return new_grid

def fold(grid: [[bool]], steps: [(str, int)], n: int = None) -> int:
    for axis, index in (steps if n is None else steps[:n]):
        if axis == 'y':
            grid = fold_vert(grid, index)
        else:
            grid = fold_horz(grid, index)
    if n is None:
        print_grid(grid)
    return sum(sum(int(cell) for cell in row) for row in grid)

dots, steps = open(argv[1]).read().split('\n\n')
dots = [tuple(map(int, line.strip().split(','))) for line in dots.strip().split('\n')]
steps = [(lambda pair: (pair[0], int(pair[1])))(line.split()[-1].split('='))
         for line in steps.strip().split('\n')]

grid = build_grid(dots)
print(fold(grid, steps, 1))
fold(grid, steps)
