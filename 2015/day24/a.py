from sys import argv
from itertools import groupby
from functools import reduce

with open(argv[1]) as fp:
    lines = fp.readlines()

weights = [int(line.strip()) for line in lines]

# adapted from https://www.geeksforgeeks.org/perfect-sum-problem-print-subsets-given-sum/
def generate_sum_subsets(arr: [int], sum_: int):
    def generate_subsets(table: [[bool]], arr: [int], i: int, sum_: int, p: [int]):
        if i == 0 and sum_ != 0 and table[0][sum_]:
            p.append(arr[i])
            yield p
            return
    
        if i == 0 and sum_ == 0:
            yield p
            return
    
        if table[i-1][sum_]:
            b = []
            b.extend(p)
            yield from generate_subsets(table, arr, i-1, sum_, b)

        if (sum_ >= arr[i] and table[i-1][sum_ - arr[i]]):
            p.append(arr[i])
            yield from generate_subsets(table, arr, i-1, sum_ - arr[i], p)
    n = len(arr)
    table = [[False for _ in range(sum_ + 1)] for _ in range(n)]
 
    for i in range(n):
        table[i][0] = True
 
    if arr[0] <= sum_:
        table[0][arr[0]] = True
 
    for i in range(1, n):
        for j in range(0, sum_ + 1):
            if arr[i] <= j:
                table[i][j] = table[i-1][j] or table[i-1][j - arr[i]]
            else:
                table[i][j] = table[i - 1][j]
 
    if table[n-1][sum_]:
        subset = []
        yield from generate_subsets(table, arr, n-1, sum_, subset)

def minimum_entanglement(weights: [int], n: int = 3):
    allocations = list(generate_sum_subsets(weights, sum(weights)//n))
    by_smallest_length_set = lambda e: len(e)
    allocations.sort(key=by_smallest_length_set)
    groups = groupby(allocations, key=by_smallest_length_set)
    return min(reduce(lambda a, b: a*b, l, 1) for l in next(groups)[1])

print(minimum_entanglement(weights))
print(minimum_entanglement(weights, 4))
