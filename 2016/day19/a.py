from sys import argv
from math import log
from collections import deque

n = int(argv[1])

def elf(n: int) -> int:
    return 1 + 2 * (n - (2 ** int(log(n, 2)))) 

print(elf(n))

def cycle_deque(n: int) -> int:
    elves = deque(range(1, n + 1))
    for n in (range(len(elves), 1, -1)):
        delta = n // 2
        elves.rotate(-delta)
        elves.popleft()
        elves.rotate(delta - 1)
    return elves[0]

def compute(n: int) -> int:
    cube = 3 ** int(log(n, 3))
    if cube == n:
        return n
    if n <= 2 * cube:
        return n - cube
    return cube + 2 * (n - 2 * cube)

print(compute(n))