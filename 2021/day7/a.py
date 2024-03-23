from sys import argv
from math import ceil, floor

def align_cost(nums: [int], uniform: bool, target: int) -> int:
    cost = 0
    for num in nums:
        diff = abs(num - target)
        cost += diff if uniform else (diff + 1) * diff // 2
    return cost

nums = [int(token) for token in open(argv[1]).read().strip().split(',')]
print(align_cost(nums, True, sorted(nums)[len(nums)//2]))
mean = sum(nums)/len(nums)
print(min(align_cost(nums, False, floor(mean)), align_cost(nums, False, ceil(mean))))
