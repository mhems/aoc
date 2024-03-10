from sys import argv
from itertools import combinations
from math import prod

def expense(nums: [int], n: int = 2):
    return next(prod(combo) for combo in combinations(nums, n) if sum(combo) == 2020)

nums = [int(line.strip()) for line in open(argv[1]).readlines()]
print(expense(nums))
print(expense(nums, 3))
