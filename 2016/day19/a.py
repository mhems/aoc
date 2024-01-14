from sys import argv
from math import log

n = int(argv[1])

def elf(n: int) -> int:
    return 1 + 2 * (n - (2 ** int(log(n, 2)))) 

print(elf(n))

def cycle(n: int) -> [int]:
    elves = list(range(1, n + 1))
    i = 0
    n = len(elves)
    while n > 1:
        delta = n // 2
        #print(i, elves[i], delta, len(elves), elves)
        elves.pop((i + delta) % n)
        i += 1
        n -= 1
        if i > n:
            i = 0
        if n % 100000 == 0:
            print('.')
    return elves[0]

print(cycle(n))

# print([cycle(i) for i in range(2, 10)])