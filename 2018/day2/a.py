from collections import Counter
from itertools import permutations

with open('input.txt') as fp:
    lines = [line.strip() for line in fp.readlines()]

def checksum(lines: [str]) -> int:
    num_doubles, num_triples = 0, 0
    for line in lines:
        freqs = Counter(line).values()
        if 2 in freqs:
            num_doubles += 1
        if 3 in freqs:
            num_triples += 1
    return num_doubles * num_triples

print(checksum(lines))

def in_common(lines: [str]) -> str:
    for a, b in permutations(lines, 2):
        same = ''.join(i for i, j in zip(a, b) if i == j)
        if len(same) + 1 == len(a):
            return same

print(in_common(lines))