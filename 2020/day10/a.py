from sys import argv

def diff_freq(nums: [int]) -> int:
    diffs = {1: 0, 3: 0}
    for i in range(len(nums) - 1):
        diffs[nums[i] - nums[i + 1]] += 1
    return diffs[1] * diffs[3]

def num_combos(nums: [int]) -> int:
    n = 0
    for i in range(1, len(nums) - 1):
        pass

nums = sorted((int(line.strip()) for line in open(argv[1]).readlines()), reverse=True)
nums.insert(0, nums[0] + 3)
nums.append(0)
print(diff_freq(nums))
print(num_combos(nums))