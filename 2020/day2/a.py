from sys import argv
from collections import Counter

def parse(line: str) -> (int, int, str, str):
    left, right = line.strip().split(': ')
    range_, c = left.split()
    l, u = map(int, range_.split('-'))
    return l, u, c, right

def part1_valid(a: int, b: int, c: str, s: str) -> bool:
    counter = Counter(s)
    return counter[c] in range(a, b + 1)

def part2_valid(a: int, b: int, c: str, s: str) -> bool:
    return 1 == sum(int(s[i-1] == c) for i in (a, b))

passwords = [parse(line.strip()) for line in open(argv[1]).readlines()]
print(sum(int(part1_valid(*pwd)) for pwd in passwords))
print(sum(int(part2_valid(*pwd)) for pwd in passwords))
