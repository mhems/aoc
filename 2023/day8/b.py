from sys import argv
from itertools import cycle
from math import lcm

with open(argv[1]) as fp:
    lines = fp.readlines()

steps = lines[0].strip()
nodes = {}
for line in lines[2:]:
    node, pair = map(lambda s: s.strip(), line.strip().split('='))
    left, right = pair.strip('()').replace(' ', '').split(',')
    nodes[node] = (left, right)

current_nodes = [node for node in nodes if node.endswith('A')]
starting_nodes = list(current_nodes)
n = 0
cycle_lengths = [0] * len(current_nodes)
for dir in cycle(steps):
    current_nodes = [nodes[node][0 if dir == 'L' else 1] for node in current_nodes]
    n += 1
    for i, node in enumerate(current_nodes):
        if node.endswith('Z'):
            cycle_lengths[i] = n
    if all(length != 0 for length in cycle_lengths):
        break

print(cycle_lengths)
print(lcm(*cycle_lengths))

