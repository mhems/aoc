import sys
from math import prod

*_, trees = open(sys.argv[1]).read().split('\n\n')
trees = [tree.split(': ') for tree in trees.splitlines()]
trees = [(prod(map(int, left.split('x'))), sum(map(int, right.split()))) for left, right in trees]
print(sum(int(qty * 3 * 3 <= area) for area, qty in trees))
