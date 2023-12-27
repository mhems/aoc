from sys import argv
from itertools import cycle

with open(argv[1]) as fp:
    lines = fp.readlines()

steps = lines[0].strip()
nodes = {}
for line in lines[2:]:
    node, pair = map(lambda s: s.strip(), line.strip().split('='))
    left, right = pair.strip('()').replace(' ', '').split(',')
    nodes[node] = (left, right)

node = 'AAA'
n = 0
for dir in cycle(steps):
    node = nodes[node][0 if dir == 'L' else 1]
    n += 1
    if node == 'ZZZ':
        break
print(n)
