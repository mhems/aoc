import sys
import math

lines = [line.rstrip('\n') for line in open(sys.argv[1]).readlines()]
ops = [op == '+' for op in lines[-1].split()]

row_wise_args = [[int(num) for num in line.split()] for line in lines[:-1]]
print(sum(sum(nums) if op else math.prod(nums) for op, *nums in zip(ops, *row_wise_args)))    

def make_col_wise_args(lines: list[str]) -> list[list[int]]:
    args = []
    i = 0
    while i < len(lines[-1]):
        cols = []
        while (i + 1 < len(lines[-1]) and lines[-1][i + 1] == ' ') or i + 1 == len(lines[-1]):
            num_str = ''.join(lines[row_index][i] for row_index in range(len(lines)-1))
            cols.append(int(num_str.strip()))
            i += 1
        i += 1
        args.append(cols)
    return args

print(sum(sum(nums) if op else math.prod(nums) for op, nums in zip(ops, make_col_wise_args(lines))))
