from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

nums = [int(line.strip()) for line in lines]

def jump(nums: [int], fancy=False):
    pos = 0
    n = len(nums)
    i = 0
    while True:
        delta = nums[pos]
        new_pos = pos + delta
        if fancy and delta >= 3:
            nums[pos] -= 1
        else:
            nums[pos] += 1
        pos = new_pos
        i += 1
        if new_pos >= n or new_pos < 0:
            break
    return i

print(jump(list(nums)))
print(jump(nums, True))