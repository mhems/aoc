from sys import argv
from itertools import takewhile, groupby

with open(argv[1]) as fp:
    lines = fp.readlines()

def str2num(s: str) -> (int, int):
    num = sum((ord(l)-ord('a')) * (26 ** i) for i, l in enumerate(reversed(s)))
    leading_as = len(list(takewhile(lambda l: l == 'a', s)))
    return (num, leading_as)

def num2str(n: int, leading: int) -> str:
    ls = []
    while n > 0:
        ls.append(n % 26)
        n //= 26
    return 'a'*leading + ''.join(chr(ord('a') + e) for e in reversed(ls))

def generate_seq(s: str):
    n, l = str2num(s)
    while True:
        n += 1
        s = num2str(n, l)
        yield s

def is_valid(s: str) -> bool:
    if any(e in s for e in 'iol'):
        return False
    num_doubles = sum(int(len(list(g)) >= 2) for _, g in groupby(s))
    if num_doubles < 2:
        return False
    triples = [s[i:i+3] for i in range(0, len(s)-2, 1)]
    return any(ord(t[0])+1 == ord(t[1]) == ord(t[2])-1 for t in triples)

def next(s: str) -> str:
    for candidate in generate_seq(s):
        if is_valid(candidate):
            return candidate

for line in lines:
    print(next(line.strip()))