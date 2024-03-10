from sys import argv
from collections import defaultdict
from itertools import product

def perms(mask: str) -> [int]:
    def substitute(s: str, indices: [int], values: [bool]) -> str:
        l = list(s)
        for i, v in zip(indices, values):
            l[i] = str(v)
        return ''.join(l)
    indices = [i for i, c in enumerate(mask) if c == 'X']
    for combo in product((0, 1), repeat=len(indices)):
        yield int(substitute(mask, indices, combo), 2)

def execute(program: [str], part1=True) -> int:
    memory = defaultdict(int)
    def write_memory(mask: str, offset: int, value: int):
        to_or = ''.join('0' if c == 'X' else c for c in mask)
        to_and = ''.join('1' if c == 'X' else c for c in mask)
        value |= int(to_or, 2)
        value &= int(to_and, 2)
        memory[offset] = value
    def write_memory2(mask: str, offset: int, value: int):
        def merge(mask_bit: str, offset_bit: str) -> str:
            if mask_bit == 'X':
                return 'X'
            return str(int(mask_bit) | int(offset_bit))
        offset = ''.join(merge(m, o) for m, o in zip(mask, bin(offset)[2:].rjust(len(mask), '0')))
        for perm in perms(offset):
            memory[perm] = value
    func = write_memory if part1 else write_memory2
    for line in program:
        if line.startswith('mask'):
            mask = line.split(' = ')[1]
        else:
            tokens = line.split(' = ')
            func(mask, int(tokens[0][4:-1]), int(tokens[1]))
    return sum(memory.values())

lines = [line.strip() for line in open(argv[1]).readlines()]
print(execute(lines))
print(execute(lines, False))
