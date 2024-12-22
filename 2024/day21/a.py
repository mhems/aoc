from sys import argv
from itertools import permutations
from functools import cache

@cache
def add(a: (int, int), b: (int, int)) -> (int, int):
    return tuple(map(sum, zip(a, b)))

@cache
def diff(a: (int, int), b: (int, int)) -> (int, int):
    return tuple(i - j for i, j in zip(a, b))

@cache
def trace(steps: str, start: (int, int), forbid: (int, int)) -> bool:
    '''return True if trace avoids forbidden position'''
    step_directions = {'^': (1, 0), '>': (0, 1), 'v': (-1, 0), '<': (0, -1)}
    pos = start
    for step in steps:
        pos = add(pos, step_directions[step])
        if pos == forbid:
            return False
    return True

def condense(seq: list) -> list:
    condensed = []
    length = 0
    i = 0
    acc = None
    while i < len(seq):
        cur = seq[i]
        if len(cur) == 1:
            length += len(cur[0])
            if acc is None:
                acc = cur[0]
            else:
                acc += cur[0]
        else:
            if acc is not None:
                condensed.append((acc, ))
            acc = None
            min_length = min(len(e) for e in cur)
            min_elements = tuple(e for e in cur if len(e) == min_length)
            condensed.append(min_elements)
            length += min_length
        i += 1
    if acc is not None:
        condensed.append((acc, ))
    return condensed, length

@cache
def numpad_sequences(code: str) -> [{str}]:
    num_positions = {
    '7': (3, 0), '8': (3, 1), '9': (3, 2),
    '4': (2, 0), '5': (2, 1), '6': (2, 2),
    '1': (1, 0), '2': (1, 1), '3': (1, 2),
                 '0': (0, 1), 'A': (0, 2)}
    pos = num_positions['A']
    path = []
    for char in code:
        dest = num_positions[char]
        dy, dx = diff(dest, pos)
        steps = ('<' if dx < 0 else '>') * abs(dx) + ('v' if dy < 0 else '^') * abs(dy)
        path.append(tuple(set(''.join(perm) + 'A' for perm in permutations(steps) if trace(perm, pos, (0, 0)))))
        pos = dest
    return condense(path)[0]

@cache
def keypad_sequence(seq: str) -> [{str}]:
    arrow_positions = {
                 '^': (1, 1), 'A': (1, 2),
    '<': (0, 0), 'v': (0, 1), '>': (0, 2)}
    pos = arrow_positions['A']
    path = []
    for char in seq:
        dest = arrow_positions[char]
        dy, dx = diff(dest, pos)
        steps = ('<' if dx < 0 else '>') * abs(dx) + ('v' if dy < 0 else '^') * abs(dy)
        path.append(tuple(set(''.join(perm) + 'A' for perm in permutations(steps) if trace(perm, pos, (1, 0)))))
        pos = dest
    return condense(path)

def robot1_sequence(seq: [{str}]) -> [{str}]:
    path = []
    for choices in seq:
        cur = set()
        for choice in choices:
            s, l = keypad_sequence(choice)
            cur.add((tuple(s), l))
        min_length = min(length for _, length in cur)
        cur = {e for e, length in cur if length == min_length}
        path.append(tuple(cur))
    return path

def pick(choice):
    print('  which do i choose', choice, '?')
    scores = [(step, keypad_sequence(step)) for step in choice]
    best_score = min(score for _, (_, score) in scores)
    best = [(c, s) for c, (s, score) in scores if score == best_score]
    print('   ', best_score, 'is shortest')
    for c, s in best:
        print('     ', c, '=>', s)
    return best_score

def robot2_sequence(seq: list) -> int:
    length = 0
    print()
    for l1 in seq:
        print(l1)
        if len(l1) == 1:
            for choice in l1[0]:
                length += pick(choice)
        else:
            sublengths = []
            for opt in l1:
                sublength = 0
                print('  opt:', opt)
                for o in opt:
                    sublength += pick(o)
                sublengths.append(sublength)
            length += min(sublengths)
    return length

def complexity(code: str) -> int:
    a = numpad_sequences(code)
    print(code, a)
    b = robot1_sequence(a)
    print(b)
    c = robot2_sequence(b)
    print('-' * 20)
    return int(code[:-1]) * c

codes = [line.strip() for line in open(argv[1]).readlines()]
print(sum(complexity(code) for code in codes))
