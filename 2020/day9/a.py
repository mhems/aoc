from sys import argv
from itertools import combinations

def invalid(num: int, nums: [int]) -> bool:
    sums = set(a + b for a, b in combinations(nums, 2))
    return num not in sums

def first_invalid(nums: [int], preamble: int = 25) -> int:
    for i in range(len(nums)):
        if invalid(nums[i+preamble], nums[i:i+preamble]):
            return nums[i+preamble]

def find_weakness(nums: [int], target: int) -> int:
    ranges = []
    cur = []
    cur.append(nums[0])
    for e in nums[1:]:
        if e >= target:
            if cur:
                ranges.append(cur)
            cur = []
        else:
            cur.append(e)
    for range in ranges:
        total = 0
        for i, start in enumerate(range):
            start_index = i
            total = start
            while total < target:
                i += 1
                total += range[i]
            if total == target:
                seq = range[start_index:i]
                return max(seq) + min(seq)

nums = [int(line.strip()) for line in open(argv[1]).readlines()]
print(first := first_invalid(nums))
print(find_weakness(nums, first))
