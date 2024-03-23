from sys import argv

def simulate(nums: [int], days: int, length: int = 7) -> int:
    for _ in range(days):
        new = 0
        for i in range(len(nums)):
            if nums[i] == 0:
                nums[i] = length - 1
                new += 1
            else:
                nums[i] -= 1
        for _ in range(new):
            nums.append(length + 1)
    return len(nums)

nums = [int(token) for token in open(argv[1]).read().strip().split(',')]
print(simulate(nums, 80))