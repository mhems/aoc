from sys import argv
from collections import namedtuple as nt

Move = nt('Move', ['name', 'a', 'b'])

with open(argv[1]) as fp:
    lines = fp.readlines()
n = int(argv[2])

def parse_move(s: str) -> Move:
    name = s[0]
    if name == 's':
        args = [int(s[1:]), None]
    elif name == 'x':
        args = [int(t) for t in s[1:].split('/')]
    else:
        args = s[1:].split('/')
    return Move(name, *args)

def exchange(s: str, i: int, j: int) -> str:
    l = list(s)
    l[i], l[j] = l[j], l[i]
    return ''.join(l)

def do_move(s: str, move: Move) -> str:
    if move.name == 's':
        return s[-move.a:] + s[:-move.a]
    elif move.name == 'x':
        return exchange(s, move.a, move.b)
    i, j = s.find(move.a), s.find(move.b)
    return exchange(s, i, j)

def dance(s: str, moves: [Move]) -> str:
    for move in moves:
        s = do_move(s, move)
    return s

moves = list(map(parse_move, lines[0].strip().split(',')))
s = ''.join(chr(i) for i in range(ord('a'), ord('a') + n))
print('part1', dance(s, moves))

def dance_repeat(s: str, moves: [Move], n: int) -> str:
    positions = [s]
    i = 0
    while True:
        s = dance(s, moves)
        i += 1
        if s in positions:
            return positions[n % i]
        positions.append(s)

print('part2', dance_repeat(s, moves, 1_000_000_000))
