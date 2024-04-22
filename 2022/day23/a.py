from sys import argv

def pad(grid: [[str]]) -> [[str]]:
    left, right = False, False
    for row in grid:
        if row[0] == '#':
            left = True
        if row[-1] == '#':
            right = True
    for y in range(len(grid)):
        tmp = grid[y]
        if left:
            tmp = ['.'] + tmp
        if right:
            tmp += ['.']
        grid[y] = tmp
    width = len(grid[0])
    if '#' in grid[0]:
        grid.insert(0, ['.'] * width)
    if '#' in grid[-1]:
        grid.append(['.'] * width)
    return grid

def elf_present(grid: [[str]], pos: (int, int)) -> bool:
    y, x = pos
    if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
        return grid[y][x] == '#'
    return False

def add(p1: (int, int), p2: (int, int)) -> (int, int):
    return tuple(a + b for a, b in zip(p1, p2))

def propose(grid: [[str]], pos: (int, int), start: int) -> (int, int):
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    neighbors = [add(pos, delta) for delta in deltas]
    presence = [elf_present(grid, neighbor) for neighbor in neighbors]
    slices = [presence[:3], presence[-3:], [presence[i] for i in (0, 3, 5)], [presence[i] for i in (2, 4, 7)]]
    indices = [1, -2, 3, 4]
    if any(presence):
        for i in range(start, start + 4):
            im = i % 4
            if not any(slices[im]):
                return neighbors[indices[im]]
    return None

def once(grid: [[str]], i: int) -> ([[str]], bool):
    propositions = []
    elves = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '#':
                propositions.append(propose(grid, (y, x), i))
                elves.append((y, x))
    moves = []
    for elf_pos, proposition in zip(elves, propositions):
        if proposition is None or propositions.count(proposition) > 1:
            pass
        else:
            moves.append((elf_pos, proposition))
    for src, dest in moves:
        grid[src[0]][src[1]] = '.'
        grid[dest[0]][dest[1]] = '#'
    return grid, bool(len(moves))

def num_empty(grid: [[str]]) -> int:
    minX, maxX, minY, maxY = 1e6, 0, 1e6, 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '#':
                minX = min(x, minX)
                maxX = max(x, maxX)
                minY = min(y, minY)
                maxY = max(y, maxY)
    return sum(grid[y][minX: maxX + 1].count('.') for y in range(minY, maxY + 1))

def conway(grid: [[str]], n: int = 10) -> int:
    i = 0
    while True:
        grid = pad(grid)
        grid, changed = once(grid, i)
        i += 1
        if i == n:
            print(num_empty(grid), flush=True)
        elif not changed:
            print(i, flush=True)
            break
        if i % 20 == 0:
            print('.', end='', flush=True)

def print_grid(grid: [[str]]):
    print('\n'.join(''.join(row) for row in grid), flush=True)
    print('-' * 60, flush=True)

grid = [list(line.strip()) for line in open(argv[1]).readlines()]
conway(grid, 10)
