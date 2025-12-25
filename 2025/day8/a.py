import sys
from math import prod
from itertools import combinations
from heapq import nlargest

nums = [tuple(map(int, line.rstrip().split(','))) for line in open(sys.argv[1]).readlines()]
pairs = sorted(combinations(nums, 2), key=lambda args: sum((a-b)**2 for a, b in zip(args[0], args[1])))
forest = []
for i, (a, b) in enumerate(pairs):
    if i == int(sys.argv[2]):
        print(prod(nlargest(3, (len(tree) for tree in forest))))
    new_forest = []
    merged = None
    placed = False
    for tree in forest:
        a_present = a in tree
        b_present = b in tree
        placed |= a_present or b_present
        if a_present ^ b_present:
            if merged is None:
                merged = set(tree)
                merged.add(a)
                merged.add(b)
            else:
                merged.update(tree)
        else:
            new_forest.append(tree)
    if merged is not None:
        new_forest.append(merged)
    elif not placed:
        new_forest.append(set((a, b)))
    forest = new_forest
    if len(forest) == 1 and len(forest[0]) == len(nums):
        print(a[0] * b[0])
        break
