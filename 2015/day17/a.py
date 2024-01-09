from sys import argv
from itertools import combinations

with open(argv[1]) as fp:
    lines = fp.readlines()

sizes = sorted(int(line.strip()) for line in lines)
amount = int(argv[2])

def num_pours(sizes: [int], amount: int) -> (int, int):
    pours = []
    for n in range(1, len(sizes) + 1):
        for combo in combinations(sizes, n):
            if sum(combo) == amount:
                pours.append(list(combo))
    min_num = min(len(pour) for pour in pours)
    count_min = sum(int(len(pour) == min_num) for pour in pours)
    return len(pours), count_min

print(num_pours(sizes, amount))