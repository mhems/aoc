from sys import argv
from functools import cache
from collections import Counter, defaultdict

@cache
def one_day(n: int) -> [int]:
    if n == 0:
        return [6, 8]
    return [n-1]

def simulate(nums: [int], n: int) -> int:
    nums = Counter(nums)
    for _ in range(n):
        new_nums = defaultdict(int)
        while nums:
            num, count = nums.popitem()
            for e in one_day(num):
                new_nums[e] += count
        nums = new_nums
    return sum(nums.values())

nums = [int(token) for token in open(argv[1]).read().strip().split(',')]
print(simulate(nums, 80))
print(simulate(nums, 256))
