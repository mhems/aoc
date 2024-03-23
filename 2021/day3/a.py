from collections import Counter
from sys import argv

def gather(nums: [str], most: bool) -> int:
    s = ''
    for i in range(len(nums[0])):
        by_freq = Counter(''.join(num[i] for num in nums)).most_common()
        s += by_freq[0][0] if most else by_freq[-1][0]
    return int(s, 2)

def filter(nums: [str], most: bool) -> int:
    s = set(nums)
    for i in range(len(nums[0])):
        by_freq = Counter(''.join(num[i] for num in s)).most_common()
        bit = by_freq[0][0] if most else by_freq[-1][0]
        if by_freq[0][1] == by_freq[-1][1]:
            bit = str(int(most))
        s = {e for e in s if e[i] == bit}
        if len(s) == 1:
            return int(s.pop(), 2)

nums = open(argv[1]).readlines()
print(gather(nums, True) * gather(nums, False))
print(filter(nums, True) * filter(nums, False))
