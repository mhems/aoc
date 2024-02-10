from sys import argv
from collections import namedtuple as nt
from itertools import permutations
import re

Node = nt('Node', ['name', 'x', 'y', 'size', 'used', 'avail', 'use'])
regex = re.compile(r'/dev/grid/node-x(\d+)-y(\d+)')

with open(argv[1]) as fp:
    lines = fp.readlines()[1:]

def parse_node(s: str) -> Node:
    def parse_size(s: str) -> int:
        return int(s[:-1])
    tokens = s.strip().split()
    match = re.match(regex, tokens[0])
    x, y = map(int, match.groups())
    return Node(tokens[0],
                x,
                y,
                parse_size(tokens[1]),
                parse_size(tokens[2]),
                parse_size(tokens[3]),
                int(tokens[4][:-1]))

def is_viable(a: Node, b: Node) -> bool:
    return a.name != b.name and a.used > 0 and a.used <= b.avail

def node_to_str(node: Node) -> str:
    return '%03s/%03s' % (node.used, node.size)

def plot(nodes: [Node], output=True) -> ((int, int), int):
    ordered = sorted(nodes, key=lambda node: (node.y, node.x))
    X = max(nodes, key=lambda node: node.x).x
    Y = max(nodes, key=lambda node: node.y).y
    avg_used = sum(node.used for node in nodes)/len(nodes)
    i = 0
    suffix = '    '
    empty = None
    for y in range(Y+1):
        for x in range(X+1):
            node = ordered[i]
            if node.use == 0:
                if output:
                    print('  */%03s' % node.size, end=suffix)
                empty = (x, y)
            elif output and node.used > 1.5 * avg_used:
                print('   #   ', end=suffix)
            elif output:
                print(node_to_str(node), end=suffix)
            i += 1
        if output:
            print()
    return empty, X

def find_shortest_path(empty_pos: (int, int), X: int) -> int:
    num_steps = 0
    if empty_pos != (X - 1, 1):
        num_steps += empty_pos[0]       # bring gap all the way left
        num_steps += empty_pos[1] - 1   # bring it up to second row
        num_steps += X - 1              # bring it to second to last column
    num_steps += 1 + 1                  # move it up and transfer data
    num_steps += (X - 1) * 5            # transfer data left, each takes 5 steps
    return num_steps

nodes = [parse_node(line.strip()) for line in lines]
print(sum(int(is_viable(*pair)) for pair in permutations(nodes, 2)))
empty, X = plot(nodes, False)
print(find_shortest_path(empty, X))