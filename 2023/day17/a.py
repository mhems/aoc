from sys import argv
from heapq import heappush, heappop

def directional_neighbor(grid: [[str]], pos: (int, int), dir: int) -> [((int, int), int)]:
    neighbors = []
    if pos[0] > 0 and dir != 2:
        neighbors.append(((pos[0] - 1, pos[1]), 0))
    if pos[0] < len(grid) - 1 and dir != 0:
        neighbors.append(((pos[0] + 1, pos[1]), 2))
    if pos[1] > 0 and dir != 1:
        neighbors.append(((pos[0], pos[1] - 1), 3))
    if pos[1] < len(grid[0]) - 1 and dir != 3:
        neighbors.append(((pos[0], pos[1] + 1), 1))
    return neighbors        

def shortest_path(grid: [[str]], min=1, max=3) -> int:
    width, height = len(grid[0]), len(grid)
    q = []
    seen = set()
    heappush(q, (0, (0, 0), 1, 1, []))
    heappush(q, (0, (0, 0), 2, 1, []))
    seen.add(((0, 0), 1, 1))
    seen.add(((0, 0), 2, 1))
    while len(q) > 0:
        heat, pos, dir, steps, path = heappop(q)
        if pos[0] == height - 1 and pos[1] == width - 1:
            if steps < min:
                continue
            return heat
        for neighbor, new_dir in directional_neighbor(grid, pos, dir):
            if new_dir != dir and steps + 1 <= min:
                continue
            new_steps = 1 if new_dir != dir else steps + 1
            if new_steps <= max:
                state = (neighbor, new_dir, new_steps)
                if state not in seen:
                    seen.add(state)
                    heappush(q, (heat + grid[neighbor[0]][neighbor[1]],
                                 neighbor,
                                 new_dir,
                                 new_steps,
                                 list(path) + [(neighbor, new_dir)]))

with open(argv[1]) as fp:
    grid = [list(map(int, line.strip())) for line in fp.readlines()]

print(shortest_path(grid))
print(shortest_path(grid, 4, 10))
