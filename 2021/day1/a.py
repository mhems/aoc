nums = [int(line.strip()) for line in open('input.txt').readlines()]
print(sum(int(nums[i+1] > nums[i]) for i in range(len(nums)-1)))
print(sum(int(sum(nums[i+1:i+4]) > sum(nums[i:i+3])) for i in range(len(nums)-3)))
