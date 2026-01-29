from sys import argv
import re

def add(p1: (int, int), p2: (int, int)) -> (int, int):
    return tuple(a + b for a, b in zip(p1, p2))

def at(grid: [[str]], pos: (int, int)) -> str:
    y, x = pos
    if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
        return grid[y][x]
    return None

def linear_wrap(grid: [[str]], pos: (int, int), facing: int) -> ((int, int), int):
    assert 0 <= facing < 4
    y, x = pos
    if facing == 0:
        x = 0
        while grid[y][x] == ' ':
            x += 1
    elif facing == 2:
        x = len(grid[0]) - 1
        while grid[y][x] == ' ':
            x -= 1
    elif facing == 1:
        y = 0
        while grid[y][x] == ' ':
            y += 1
    else:
        y = len(grid) - 1
        while grid[y][x] == ' ':
            y -= 1
    return (y, x), facing

def cubic_wrap(_grid: [[str]], pos: (int, int), facing: int, square_size: int = 50) -> ((int, int), int):
    '''
            +---+- -+
            | B | A |
            +---+---+
            | C |
        +---+---+
        | E | D |
        +---+---+
        | F |
        +---+
    '''
    y, x = pos
    sy, sx = y // square_size, x // square_size
    ry, rx = y % square_size, x % square_size
    
    assert 0 <= sx <= 3
    assert 0 <= sy <= 4
    assert 0 <= facing < 4

    if sy == 0:
        if sx == 1:
            # B
            if 0 <= facing <= 1:
                assert False
            elif facing == 2:
                return (2*square_size + square_size - ry - 1, 0), 0
            else:
                return (3*square_size + rx, 0), 0
        elif sx == 2:
            # A
            if facing == 0:
                return (2*square_size + square_size - ry - 1, 2*square_size - 1), 2
            elif facing == 1:
                return (square_size + rx, 2*square_size - 1), 2
            elif facing == 2:
                assert False
            else:
                return (4*square_size - 1, rx), 3
        else:
            assert False
    elif sy == 1:
        # C
        assert sx == 1
        if facing == 0:
            return (square_size - 1, 2*square_size + ry), 3
        elif facing == 1:
            assert False
        elif facing == 2:
            return (2*square_size, ry), 1
        else:
            assert False
    elif sy == 2:
        if sx == 0:
            # E
            if 0 <= facing <= 1:
                assert False
            elif facing == 2:
                return (square_size - ry - 1, square_size), 0
            else:
                return (square_size + rx, square_size), 0
        elif sx == 1:
            # D
            if facing == 0:
                return (square_size - ry - 1, 3*square_size - 1), 2
            elif facing == 1:
                return (3*square_size + rx, square_size - 1), 2
            elif facing >= 2:
                assert False
        else:
            assert False
    elif sy == 3:
        if sx == 0:
            # F
            if facing == 0:
                return (3*square_size - 1, square_size + ry), 3
            elif facing == 1:
                return (0, 2*square_size + rx), 1
            elif facing == 2:
                return (0, square_size + ry), 1
            else:
                assert False
        else:
            assert False       

def move(grid: [[str]], pos: (int, int), facing: int, amt: int, linear: bool) -> ((int, int), int):
    count = 0
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    delta = deltas[facing]
    func = linear_wrap if linear else cubic_wrap
    def handle_wrap(pos: (int, int), facing: int, todo: int) -> ((int, int), int):
        a, f = func(grid, pos, facing)
        if at(grid, a) == '#':
            return pos, facing
        return move(grid, a, f, todo, linear)
    while count < amt and at(grid, add(pos, delta)) == '.':
        pos = add(pos, delta)
        count += 1
    next = at(grid, add(pos, delta))
    if count == amt or next == '#':
        return pos, facing
    if next in (None, ' '):
        new_pos, new_facing = handle_wrap(pos, facing, amt - count - 1)
        return new_pos, new_facing
    raise ValueError('unexpected state: ' + next)

def walk(grid: [[str]], path, linear: bool = True) -> int:
    pos = (0, grid[0].index('.'))
    facing = 0
    for step in path:
        if isinstance(step, int):
            pos, facing = move(grid, pos, facing, step, linear)
        else:
            if step == 'L':
                facing = (facing - 1) % 4
            else:
                facing = (facing + 1) % 4
    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + facing

grid, steps = open(argv[1]).read().split('\n\n')
grid = [list(row) for row in grid.split('\n')]
width = max(len(row) for row in grid)
grid = [row + [' '] * (width - len(row)) for row in grid]
path = list(map(lambda e: int(e) if e[0].isdigit() else e, re.findall(r'\d+|[LR]', steps.strip())))
print(walk(grid, path))
print(walk(grid, path, False))
