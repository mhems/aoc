from sys import argv
from itertools import product
from tqdm import tqdm

def generate_combos(pattern: str) -> int:
    def substitute(s: str, indices: [int], values: [bool]) -> str:
        l = list(s)
        for i, v in zip(indices, values):
            l[i] = '.' if v else '#'
        return ''.join(l)
    indices = [i for i, c in enumerate(pattern) if c == '?']
    for combo in product((True, False), repeat=pattern.count('?')):
        yield substitute(pattern, indices, combo)

def is_valid(s: str, groups: [int]) -> bool:
    runs = list(filter(None, s.split('.')))
    if len(runs) != len(groups):
        return False
    return all(span == len(run) for span, run in zip(groups, runs))

def count_arrangements_naive(line: str) -> int:
    left, right = line.split()
    groups = [int(e) for e in right.split(',')]
    return sum(int(is_valid(combo, groups)) for combo in generate_combos(left))

with open(argv[1]) as fp:
    lines = [line.strip() for line in fp.readlines()]

print(sum(count_arrangements_naive(line) for line in tqdm(lines)))
