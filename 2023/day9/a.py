from sys import argv
from itertools import pairwise

with open(argv[1]) as fp:
    lines = fp.readlines()

nums = [list(map(int, line.split())) for line in lines]

def diff_list(nums: [int]):
    return list(map(lambda pair: pair[1] - pair[0], pairwise(nums)))

def make_diff_lists(nums: [int]) -> [[int]]:
    diffs = [nums, diff_list(nums)]
    while not all(e == 0 for e in diffs[-1]):
        diffs.append(diff_list(diffs[-1]))
    return diffs

def find_next_missing_number(nums: [int]) -> int:
    diffs = make_diff_lists(nums)
    for i in range(len(diffs) - 2, -1, -1):
        diffs[i].append(diffs[i+1][-1] + diffs[i][-1])
    return diffs[0][-1]

answer = sum(find_next_missing_number(seq) for seq in nums)
print(answer)

def find_prev_missing_number(nums: [int]) -> int:
    diffs = make_diff_lists(nums)
    for i in range(len(diffs) - 2, -1, -1):
        diffs[i].insert(0, diffs[i][0] - diffs[i+1][0])
    return diffs[0][0]

answer = sum(find_prev_missing_number(seq) for seq in nums)
print(answer)