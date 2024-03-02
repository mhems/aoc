from sys import argv

def find_start(grid: [[str]]) -> (int, int):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'S':
                return (y, x)

def vacant_neighbors(grid: [[str]], pos: (int, int)) -> [(int, int)]:
    neighbors = []
    if pos[0] < len(grid) - 1:
        neighbors.append((pos[0] + 1, pos[1]))
    if pos[0] > 0:
        neighbors.append((pos[0] - 1, pos[1]))
    if pos[1] < len(grid[0]) - 1:
        neighbors.append((pos[0], pos[1] + 1))
    if pos[1] > 0:
        neighbors.append((pos[0], pos[1] - 1))
    return [(y, x) for y, x in neighbors if grid[y][x] != '#']

def reachable_from(grid: [[str]], positions: [(int, int)]) -> [(int, int)]:
    reachable = set()
    for position in positions:
        for neighbor in vacant_neighbors(grid, position):
            reachable.add(neighbor)
    return reachable

def num_reachable(grid: [[str]], start: (int, int), n: int) -> int:
    positions = [start]
    for _ in range(n):
        positions = reachable_from(grid, positions)
    return len(positions)

with open(argv[1]) as fp:
    grid = [list(line.strip()) for line in fp.readlines()]

start = find_start(grid)
print(num_reachable(grid, start, 64))
