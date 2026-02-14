from sys import argv
from itertools import permutations
from functools import cache

@cache
def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return tuple(map(sum, zip(a, b)))

@cache
def diff(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return tuple(i - j for i, j in zip(a, b))

@cache
def trace(steps: str, start: tuple[int, int], forbidden: tuple[int, int]) -> bool:
    '''return True if trace avoids forbidden position'''
    step_directions = {'^': (1, 0), '>': (0, 1), 'v': (-1, 0), '<': (0, -1)}
    pos = start
    for step in steps:
        pos = add(pos, step_directions[step])
        if pos == forbidden:
            return False
    return True

def generate_positions(code: str, positions: dict[str, tuple[int, int]], forbidden: tuple[int, int]) -> tuple[tuple[str]]:
    pos = positions['A']
    path = []
    for char in code:
        dest = positions[char]
        dy, dx = diff(dest, pos)
        steps = ('<' if dx < 0 else '>') * abs(dx) + ('v' if dy < 0 else '^') * abs(dy)
        path.append(list(set(''.join(perm) + 'A' for perm in permutations(steps) if trace(perm, pos, forbidden))))
        pos = dest
    return tuple(tuple(step) for step in path)

def numpad_sequences(code: str) -> tuple[tuple[str]]:
    num_positions = {
    '7': (3, 0), '8': (3, 1), '9': (3, 2),
    '4': (2, 0), '5': (2, 1), '6': (2, 2),
    '1': (1, 0), '2': (1, 1), '3': (1, 2),
                 '0': (0, 1), 'A': (0, 2)}
    return generate_positions(code, num_positions, (0, 0))

@cache
def keypad_sequence(code: str) -> tuple[tuple[str]]:
    arrow_positions = {
                 '^': (1, 1), 'A': (1, 2),
    '<': (0, 0), 'v': (0, 1), '>': (0, 2)}
    return generate_positions(code, arrow_positions, (1, 0))

@cache
def min_presses(codes: tuple[tuple[str]], n: int) -> int:
    total = 0
    for step in codes:
        if len(step) == 1:
            if n == 0:
                total += len(step[0])
            else:
                total += min_presses(keypad_sequence(step[0]), n - 1)
        else:
            if n == 0:
                options = [len(opt) for opt in step]
            else:
                options = [min_presses(keypad_sequence(opt), n - 1) for opt in step]
            total += min(options)
    return total

def complexity(code: str, n: int) -> int:
    return int(code[:-1]) * min_presses(numpad_sequences(code), n)

codes = [line.strip() for line in open(argv[1]).readlines()]

print(sum(complexity(code, 2) for code in codes))
print(sum(complexity(code, 25) for code in codes))
