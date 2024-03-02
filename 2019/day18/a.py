from sys import argv
import heapq

def parse_grid() -> ([[str]], {str: (int, int)}):
    with open(argv[1]) as fp:
        lines = [list(line.strip()) for line in fp.readlines()]
    objects = {}
    for y, row in enumerate(lines):
        for x, cell in enumerate(row):
            if cell not in ('#', '.'):
                objects[cell] = (y, x)
    return lines, objects

def is_door(grid: [[str]], value) -> bool:
    if isinstance(value, tuple):
        return is_door(None, grid[value[0]][value[1]])
    return 'A' <= value <= 'Z'

def is_key(grid: [[str]], value) -> bool:
    if isinstance(value, tuple):
        return is_key(None, grid[value[0]][value[1]])
    return 'a' <= value <= 'z'

def is_blocked(grid: [[str]], pos: (int, int), keys: {int}) -> bool:
    cell = grid[pos[0]][pos[1]]
    if cell == '#':
        return True
    if cell == '.':
        return False
    return is_door(grid, pos) and cell.lower() not in keys

neighbors = {}
def vacant_neighbors(grid: [[str]], pos: (int, int), keys: {int}) -> [(int, int)]:
    global neighbors
    if pos not in neighbors:  
        legal_positions = []
        if pos[0] > 0:
            legal_positions.append((pos[0] -1, pos[1]))
        if pos[0] < len(grid) - 1:
            legal_positions.append((pos[0] + 1, pos[1]))
        if pos[1] > 0:
            legal_positions.append((pos[0], pos[1] - 1))
        if pos[1] < len(grid[0]) - 1:
            legal_positions.append((pos[0], pos[1] + 1))
        neighbors[pos] = legal_positions
    legal_positions = neighbors[pos]
    return [(y, x) for y, x in legal_positions if not is_blocked(grid, (y, x), keys)]

def gated_bfs(grid: [[str]], num_keys: int, start: (int, int)) -> int:
    q = []
    heapq.heappush(q, (0, start, set(), 0))
    visited = set()
    visited.add((start, tuple()))
    max_keys = 0
    while len(q) > 0:
        _, pos, keys, steps = heapq.heappop(q)
        if is_key(grid, pos):
            keys.add(grid[pos[0]][pos[1]])
        if len(keys) == num_keys:
            return steps
        if len(keys) > max_keys:
            max_keys = len(keys)
            print('found', max_keys, len(q), len(visited))
        for neighbor in vacant_neighbors(grid, pos, keys):
            state = (neighbor, tuple(keys))
            if state not in visited:
                visited.add(state)
                heapq.heappush(q, (steps - len(keys), neighbor, set(keys), steps + 1))

def quadsect(grid: [[str]], start: (int, int)) -> [[str]]:
    y, x = start
    grid[y-1][x-1] = '@'
    grid[y-1][x] = '#'
    grid[y-1][x+1] = '@'
    grid[y][x] = '#'
    grid[y][x-1] = '#'
    grid[y][x+1] = '#'
    grid[y+1][x-1] = '@'
    grid[y+1][x] = '#'
    grid[y+1][x+1] = '@'
    return grid, [(y-1, x-1), (y-1, x+1), (y+1, x-1), (y+1, x+1)]    

def quad_bfs(grid: [[str]], num_keys: int, starts: [(int, int)]) -> int:
    q = []
    heapq.heappush(q, (0, starts, set(), 0))
    visited = set()
    visited.add((tuple(starts), tuple()))
    max_keys = 0
    while len(q) > 0:
        _, positions, keys, steps = heapq.heappop(q)
        for pos in positions:
            if is_key(grid, pos):
                keys.add(grid[pos[0]][pos[1]])
        if len(keys) == num_keys:
            return steps
        if len(keys) > max_keys:
            max_keys = len(keys)
            print('found', max_keys, len(q), len(visited))
        for i, pos in enumerate(positions):
            for neighbor in vacant_neighbors(grid, pos, keys):
                new_positions = list(positions)
                new_positions[i] = neighbor
                state = (tuple(new_positions), tuple(keys))
                if state not in visited:
                    visited.add(state)
                    heapq.heappush(q,
                                   (steps - len(keys),
                                    new_positions,
                                    set(keys),
                                    steps + 1))

grid, objects = parse_grid()
start = objects.pop('@')
num_keys = sum(int(is_key(None, object)) for object in objects.keys())
#print(gated_bfs(grid, num_keys, start))
grid, starts = quadsect(grid, start)
print(quad_bfs(grid, num_keys, starts))
