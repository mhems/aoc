from sys import argv

def print_grid(grid: [[str]]):
    print('\n'.join(''.join(row) for row in grid))

def find_start(grid: [[str]]) -> (int, int):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '@':
                grid[y][x] = '.'
                return y, x

def add(pos: (int, int), delta: (int, int)) -> (int, int):
    return tuple(map(sum, zip(pos, delta)))

def move_one(grid: [[str]], pos: (int, int), step: str) -> (int, int):
    initial = pos
    y, x = add(pos, step)
    if grid[y][x] == '#':
        return pos
    elif grid[y][x] == '.':
        return y, x
    elif grid[y][x] == 'O':
        original = y, x
        while grid[y][x] == 'O':
            pos = add(pos, step)
            y, x = pos
        if grid[y][x] == '.':
            grid[y][x] = 'O'
            grid[original[0]][original[1]] = '.'
            return original
    elif grid[y][x] in ['[', ']']:
        pass # TODO
    return initial

def move(grid: [[str]], steps: [str]):
    pos = find_start(grid)
    deltas = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
    for step in steps:
        pos = move_one(grid, pos, deltas[step])

def box_sum(grid: [[str]]) -> int:
    total = 0
    width = len(grid[0])
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'O':
                total += 100 * y + x
            elif cell in '[':
                total += 100 * y + min(x, width - 1 - x - 1)
    return total

def expand(grid: [str]) -> [[str]]:
    return [list(row.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')) for row in grid]

a, b = open(argv[1]).read().split('\n\n')
text = [line.strip() for line in a.strip().split('\n')]
grid = [list(line) for line in text]
steps = b.replace('\n', '').strip()

move(grid, steps)
print_grid(grid)
print(box_sum(grid))

grid = expand(text)
move(grid, steps)
print_grid(grid)
print(box_sum(grid))
