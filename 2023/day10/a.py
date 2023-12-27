from sys import argv
from collections import namedtuple as nt

Pos = nt('Pos', ['x', 'y'])

def find_start(field: [[str]]) -> Pos:
    for i, row in enumerate(field):
        try:
            j = row.index('S')
            return Pos(j, i)
        except ValueError:
            continue

def get(field: [[str]], pos: Pos) -> str:
    return field[pos.y][pos.x]

def get_moves(field: [[str]], pos: Pos) -> [Pos, Pos]:
    '''at every position in the loop, there are two positions to move to'''
    moves = []
    cur_val = get(field, pos)
    # west
    if pos.x > 0:
        cand = Pos(pos.x - 1, pos.y)
        cand_val = get(field, cand)
        if cur_val in '-J7S' and cand_val in '-LFS':
            moves.append(cand)
    # east
    if pos.x < len(field[0]) - 1:
        cand = Pos(pos.x + 1, pos.y)
        cand_val = get(field, cand)
        if cur_val in '-LFS' and cand_val in '-J7S':
            moves.append(cand)
    # north
    if pos.y > 0:
        cand = Pos(pos.x, pos.y - 1)
        cand_val = get(field, cand)
        if cur_val in '|LJS' and cand_val in '|7FS':
            moves.append(cand)
    # south
    if pos.y < len(field) - 1:
        cand = Pos(pos.x, pos.y + 1)
        cand_val = get(field, cand)
        if cur_val in '|7FS' and cand_val in '|LJS':
            moves.append(cand)
    return moves

def move_one(field: [[str]], curPos: Pos, lastPos: [Pos]) -> Pos:
    moves = get_moves(field, curPos)
    #print('cur', curPos, get(field, curPos), 'moves', moves, 'last', lastPos)
    if lastPos is None or (len(moves) == 1 and moves[0] != lastPos):
        return moves[0]
    moves.remove(lastPos)
    return moves[0]

def move(field: [[str]], start: Pos) -> [Pos]:
    history = [None]
    curPos = start
    nextPos = None
    while nextPos != start:
        nextPos = move_one(field, curPos, history[-1])
        history.append(curPos)
        curPos = nextPos
    history.pop(0)
    return history

with open(argv[1]) as fp:
    lines = fp.readlines()

matrix = [list(line.strip()) for line in lines]
start = find_start(matrix)

loop = move(matrix, start)
furthest = len(loop)//2
print(furthest)
