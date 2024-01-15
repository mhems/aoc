from sys import argv
from collections import namedtuple as nt
from itertools import permutations

Size = nt('Size', ['amount', 'repr'])
Node = nt('Node', ['name', 'size', 'used', 'avail', 'use'])

with open(argv[1]) as fp:
    lines = fp.readlines()
lines = lines[2:]

def parse_size(s: str) -> Size:
    amount = int(s[:-1])
    suffix = s[-1]
    if suffix == 'T':
        amount *= 1024 ** 4
    elif suffix == 'G':
        amount *= 1024 ** 3
    elif suffix == 'M':
        amount *= 1024 ** 2
    elif suffix == 'K':
        amount *= 1024
    return Size(amount, s)

def parse_node(s: str) -> Node:
    tokens = s.strip().split()
    return Node(tokens[0], parse_size(tokens[1]), parse_size(tokens[2]), parse_size(tokens[3]), int(tokens[4][:-1]))

def is_viable(a: Node, b: Node) -> bool:
    return a.name != b.name and a.used.amount > 0 and a.used.amount <= b.avail.amount

nodes = [parse_node(line.strip()) for line in lines]
print(sum(int(is_viable(*pair)) for pair in permutations(nodes, 2)))
