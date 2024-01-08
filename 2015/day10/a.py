from sys import argv
from itertools import groupby

with open(argv[1]) as fp:
    lines = fp.readlines()

def cycle(n: str) -> str:
    return "".join(str(len(list(g))) + str(k) for k, g in groupby(n))

def process(s: str, n: int) -> int:
    for _ in range(n):
        s = cycle(s)
    return len(s)

num = lines[0].strip()
print(process(num, 40))
print(process(num, 50))