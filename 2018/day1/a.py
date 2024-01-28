from itertools import cycle

with open('input.txt') as fp:
    lines = fp.readlines()

nums = [int(line.strip()) for line in lines]
print(sum(nums))

def seen_again_first(nums: [int]) -> int:
    seen = set()
    total = 0
    for num in cycle(nums):
        total += num
        if total in seen:
            return total
        seen.add(total)

print(seen_again_first(nums))
