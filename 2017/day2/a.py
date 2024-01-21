from itertools import permutations

with open('input.txt') as fp:
    lines = fp.readlines()

total = 0
for line in lines:
    nums = list(map(int, line.strip().split()))
    total += max(nums) - min(nums)
print(total)

total = 0
for line in lines:
    nums = list(map(int, line.strip().split()))
    for a, b in permutations(nums, 2):
        if a % b == 0:
            total += a // b
            break
        elif b % a == 0:
            total += b // a
            break
print(total)
