from sys import argv
from math import prod

def count_trees(grid: [str], dy=1, dx=3) -> int:
    return sum(('#' == grid[i][dx*i//dy % len(grid[0])]) for i in range(1, len(grid)) if i % dy == 0)

def all_slopes(grid: [str]) -> int:
    return prod(count_trees(grid, y, x) for y, x in ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1)))
    
grid = [line.strip() for line in open(argv[1]).readlines()]
print(count_trees(grid))
print(all_slopes(grid))
