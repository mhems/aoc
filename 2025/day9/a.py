import sys
from itertools import combinations
from math import prod

coords = [tuple(map(int, line.rstrip().split(','))) for line in open(sys.argv[1]).readlines()]
combos = list(combinations(coords, 2))
print(max(prod(abs(i-j) + 1 for i, j in zip(*combo)) for combo in combos))
