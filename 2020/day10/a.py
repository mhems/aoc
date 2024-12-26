from sys import argv
from itertools import pairwise, groupby
from collections import Counter

def diff_freq(diffs: [int]) -> int:
    num_ones = sum(int(diff == 1) for diff in diffs)
    return num_ones * (len(diffs) - num_ones)

def num_combos(diffs: [int]) -> int:
    counts = Counter(len(tuple(g)) for k, g in groupby(diffs, lambda e: e == 1) if k)
    counts.pop(1)
    product = 1
    for length, freq in counts.items():
        if length == 2:
            product *= 2 ** freq
        elif length == 3:
            product *= 4 ** freq
        elif length == 4:
            product *= 7 ** freq
    return product

nums = sorted((int(line.strip()) for line in open(argv[1]).readlines()), reverse=True)
nums.insert(0, nums[0] + 3)
nums.append(0)
diffs = [a - b for a, b in pairwise(nums)]
print(diff_freq(diffs))
print(num_combos(diffs))
