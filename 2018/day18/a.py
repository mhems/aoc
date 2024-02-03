from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

def neighbors_num(grid: [str], x: int, y: int) -> (int, int):
    deltas = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    neighbors = [grid[y + dy][x + dx] for dx, dy in deltas]
    return sum(int(cell == '|') for cell in neighbors), sum(int(cell == '#') for cell in neighbors)

def parse_grid(lines: [str]) -> [[str]]:
    grid = [['.'] + list(line.strip()) + ['.'] for line in lines]
    grid.insert(0, ['.'] * len(grid[0]))
    grid.append(['.'] * len(grid[0]))
    return grid

def change(grid: [[str]]) -> [[str]]:
    new_grid = [['.'] * len(grid[0]) for _ in range(len(grid))]
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
            num_trees, num_lumber = neighbors_num(grid, x, y)
            cell = grid[y][x]
            if cell == '.' and num_trees >= 3:
                new_grid[y][x] = '|'
            if cell == '|':
                new_grid[y][x] = '#' if num_lumber >= 3 else '|'
            if cell == '#' and num_lumber >= 1 and num_trees >= 1:
                new_grid[y][x] = '#'
    return new_grid

def resource_value(grid: [[str]]) -> int:
    num_trees, num_lumber = 0, 0
    for row in grid:
        for cell in row:
            if cell == '|':
                num_trees += 1
            elif cell == '#':
                num_lumber += 1
    return num_trees * num_lumber

def to_str(grid: [[str]]) -> str:
    return ''.join(''.join(grid[y][x] for x in range(1, len(grid[0])-1))
                   for y in range(1, len(grid)-1))

def iterate(grid: [[str]], n: int) -> int:
    for _ in range(n):
        grid = change(grid)
    return resource_value(grid)

grid = parse_grid(lines)
print(iterate(grid, 10))
