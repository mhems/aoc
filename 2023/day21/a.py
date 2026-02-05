from sys import argv

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

def reachable(grid: [[str]], start: (int, int), ns: int) -> [int]:
    positions = {start}
    lengths = []
    singular = False
    if isinstance(ns, int):
        ns = [ns]
        singular = True
    for i in range(max(ns)):
        positions = reachable_from(grid, positions)
        if i + 1 in ns:
            lengths.append(len(positions))
    return lengths[0] if singular else lengths

grid = [list(line.strip()) for line in open(argv[1]).readlines()]
D = len(grid)
d = D//2
start = d, d

print(reachable(grid, start, 64))

num_steps = 26501365
radius = (num_steps - d) // D
radius_complete = radius - 1
B, A = reachable(grid, start, [2*D, 2*D+1])
total = A * (radius_complete**2) + B * (radius**2)

# the below is with credit to https://www.youtube.com/watch?v=9UOMZSL0JTg

starts = [(0, 0), (0, D-1), (D-1, 0), (D-1, D-1)]
for start in starts:
    total += radius_complete * reachable(grid, start, D+d-1)
    total += radius * reachable(grid, start, d-1)

corners = [(D-1, d), (d, 0), (0, d), (d, D-1)]
for corner in corners:
    total += reachable(grid, corner, D-1)
    
print(total)
