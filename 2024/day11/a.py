from sys import argv
from functools import cache
from collections import Counter, defaultdict

@cache
def blink(i: int) -> [int]:
    if i == 0:
        return [1]
    str_ = str(i)
    N = len(str_)
    if N % 2 == 0:
        return [int(str_[:N//2]), int(str_[N//2:])]
    return [i * 2024]

def blink_many(stones: [int], n: int) -> int:
    stones = Counter(stones)
    for _ in range(n):
        new_stones = defaultdict(int)
        while stones:
            stone, count = stones.popitem()
            for e in blink(stone):
                new_stones[e] += count
        stones = new_stones
    return sum(stones.values())

stones = [int(stone) for stone in open(argv[1]).read().strip().split()]
print(blink_many(stones, 25))
print(blink_many(stones, 75))
