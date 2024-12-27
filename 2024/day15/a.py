from sys import argv

def print_grid(grid: [[str]], pos = None):
    if pos is None:
        print('\n'.join(''.join(row) for row in grid))
    else:
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if (y, x) == pos:
                    print('@', end='')
                else:
                    print(cell, end='')
            print()
    print(flush=True)

def find_start(grid: [[str]]) -> (int, int):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '@':
                grid[y][x] = '.'
                return y, x

def add(pos: (int, int), delta: (int, int)) -> (int, int):
    return tuple(map(sum, zip(pos, delta)))

def recurse(grid: [[str]], pos: (int, int), step: (int, int), todo: {(int, int)}) -> bool:
    y, x = pos
    left, right = ((y, x), (y, x + 1)) if grid[y][x] == '[' else ((y, x - 1), (y, x))
    new_left, new_right = add(left, step), add(right, step)
    ly, lx = new_left
    ry, rx = new_right
    left_cell, right_cell = grid[ly][lx], grid[ry][rx]
    if left_cell == '#' or right_cell == '#':
        return False
    todo.add((new_left))
    todo.add((new_right))
    if left_cell == '.' and right_cell == '.':
        return True
    elif left_cell == '#' or right_cell == '#':
        return False
    elif left_cell == '[' and right_cell == ']':
        return recurse(grid, new_left, step, todo)
    elif left_cell == ']':
        if right_cell == '[':
            return recurse(grid, new_left, step, todo) and recurse(grid, new_right, step, todo)
        elif right_cell == '.':
            return recurse(grid, new_left, step, todo)
    elif left_cell == '.':
        return recurse(grid, new_right, step, todo)

def move_one(grid: [[str]], pos: (int, int), step: (int, int)) -> (int, int):
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
    elif grid[y][x] in '[]':
        original = y, x
        if step[0] == 0: # horizontal
            while grid[y][x] in '[]':
                pos = add(pos, step)
                y, x = pos
            if grid[y][x] == '.':
                reverse = (0, -1 * step[1])
                while pos != original:
                    next = add(pos, reverse)
                    grid[y][pos[1]] = grid[y][next[1]]
                    pos = next
                grid[y][pos[1]] = '.'
                return pos
        else: # vertical
            todo = set()
            if recurse(grid, (y, x), step, todo):
                d = -step[0]
                original = {(y+d, x): grid[y+d][x] for y, x in todo}
                for (a, b) in sorted(todo, key=lambda pos: pos[0], reverse= d == -1):
                    grid[a][b] = original[(a+d, b)]
                    grid[a+d][b] = '.'
                return (y, x)
    return initial

def move(grid: [[str]], steps: [str]):
    pos = find_start(grid)
    deltas = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
    for step in steps:
        pos = move_one(grid, pos, deltas[step])

def box_sum(grid: [[str]]) -> int:
    total = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in 'O[':
                total += 100 * y + x
    return total

def expand(grid: [str]) -> [[str]]:
    return [list(row.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')) for row in grid]

a, b = open(argv[1]).read().split('\n\n')
text = [line.strip() for line in a.strip().split('\n')]
grid = [list(line) for line in text]
steps = b.replace('\n', '').strip()

move(grid, steps)
#print_grid(grid)
print(box_sum(grid))

grid = expand(text)
#print_grid(grid)
move(grid, steps)
#print_grid(grid)
print(box_sum(grid))
