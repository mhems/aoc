from sys import argv
from functools import reduce

with open(argv[1]) as fp:
    lines = fp.readlines()
    
times = list(map(int, lines[0].strip().split()[1:]))
distances = list(map(int, lines[1].strip().split()[1:]))
stats = zip(times, distances)

def distance(r: int, t: int) -> int:
    return r * (t - r)

def count_wins(pair: (int, int)) -> int:
    return sum(1 for r in range(1, pair[0]) if distance(r, pair[0]) > pair[1])

answer = reduce(lambda a, b: a * b, map(count_wins, stats))
print(answer)

time = int(''.join(lines[0].strip().split()[1:]))
dist = int(''.join(lines[1].strip().split()[1:]))

print(count_wins((time, dist)))
