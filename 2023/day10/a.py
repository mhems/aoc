from sys import argv
from collections import deque

def find_start(field: [[str]]) -> (int, int):
    for i, row in enumerate(field):
        try:
            j = row.index('S')
            return (i, j)
        except ValueError:
            continue

def get_moves(field: [[str]], pos: (int, int)) -> [(int, int), (int, int)]:
    '''at every position in the loop, there are two positions to move to'''
    moves = []
    y, x = pos
    cur_val = field[y][x]
    if x > 0:
        cand = (y, x - 1)
        cand_val = field[cand[0]][cand[1]]
        if cur_val in '-J7S' and cand_val in '-LFS':
            moves.append(cand)
    if x < len(field[0]) - 1:
        cand = (y, x + 1)
        cand_val = field[cand[0]][cand[1]]
        if cur_val in '-LFS' and cand_val in '-J7S':
            moves.append(cand)
    if y > 0:
        cand = (y - 1, x)
        cand_val = field[cand[0]][cand[1]]
        if cur_val in '|LJS' and cand_val in '|7FS':
            moves.append(cand)
    if y < len(field) - 1:
        cand = (y + 1, x)
        cand_val = field[cand[0]][cand[1]]
        if cur_val in '|7FS' and cand_val in '|LJS':
            moves.append(cand)
    return moves

def move_one(field: [[str]], curPos: (int, int), lastPos: [(int, int)]) -> (int, int):
    moves = get_moves(field, curPos)
    if lastPos is None or (len(moves) == 1 and moves[0] != lastPos):
        return moves[0]
    moves.remove(lastPos)
    return moves[0]

def move(field: [[str]], start: (int, int)) -> [(int, int)]:
    history = [None]
    curPos = start
    nextPos = None
    while nextPos != start:
        nextPos = move_one(field, curPos, history[-1])
        history.append(curPos)
        curPos = nextPos
    history.pop(0)
    return history

def print_field(matrix: [[str]], loop: [(int, int)]):
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if (y, x) in loop:
                if cell == '7':
                    a = '2510'
                elif cell == 'J':
                    a = '2518'
                elif cell == 'L':
                    a = '2514'
                elif cell == 'F':
                    a = '250C'
                elif cell == '-':
                    a = '2500'
                elif cell == '|':
                    a = '2502'
                print(chr(int(a, 16)), end='')
            else:
                print('*', end='')
        print()

def print_matrix(matrix: [[str]], loop: [(int, int)]):
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if (y, x) in loop:
                print(cell, end='')
            else:
                print('*', end='')
        print()

def transform(matrix: [[str]], loop: [(int, int)]) -> [[str]]:
    transformed = []
    for y, row in enumerate(matrix):
        a = ''
        b = ''
        c = ''
        for x, cell in enumerate(row):
            if (y, x) in loop:
                if cell == '7':
                    a += '   '
                    b += '## '
                    c += ' # '
                elif cell == 'F':
                    a += '   '
                    b += ' ##'
                    c += ' # '
                elif cell == 'J':
                    a += ' # '
                    b += '## '
                    c += '   '
                elif cell == 'L':
                    a += ' # '
                    b += ' ##'
                    c += '   '
                elif cell in '-S': # S is '-' in my input
                    a += '   '
                    b += '###'
                    c += '   '
                elif cell == '|':
                    a += ' # '
                    b += ' # '
                    c += ' # '
            else:
                a += '   '
                b += ' O '
                c += '   '
        transformed.append(a)
        transformed.append(b)
        transformed.append(c)
    return transformed

def print_grid(grid: [[str]]):
    for row in grid:
        print(''.join(row))

def neighbors(pos: (int, int), Y: int, X: int) -> [(int, int)]:
    deltas = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    y, x = pos
    return [(y + dy, x + dx) for dy, dx in deltas if 0 <= y + dy < Y and 0 <= x + dx < X]

def flood_fill(grid: [[str]], start: (int, int), Y: int, X: int) -> {(int, int)}:
    visited = {start}
    q = deque([start])
    while q:
        pos = q.popleft()
        for n in neighbors(pos, Y, X):
            if grid[n[0]][n[1]] != '#' and n not in visited:
                visited.add(n)
                q.append(n)
    return visited

def num_enclosed_cells(matrix: [[str]], loop: [(int, int)]) -> int:
    transformed = transform(matrix, loop)
    exterior = flood_fill(transformed, (0, 0), len(transformed), len(transformed[0]))
    return sum(sum(cell == 'O' for x, cell in enumerate(row) if (y, x) not in exterior)
               for y, row in enumerate(transformed))

matrix = [list(line.strip()) for line in open(argv[1]).readlines()]
start = find_start(matrix)
#print_grid(matrix)
loop = move(matrix, start)
print(len(loop)//2)
#print_matrix(matrix, loop)
print(num_enclosed_cells(matrix, loop))
