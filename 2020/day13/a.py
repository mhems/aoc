from sys import argv
from math import gcd
from functools import reduce

def first_departure(earliest: int, busses: [int]) -> int:
    time = earliest
    while True:
        for bus in busses:
            if time % bus == 0:
                return (time - earliest) * bus
        time += 1

# https://www.dcode.fr/bezout-identity
def bezout(a: int, b: int) -> (int, int):
    u, v, up, vp = 1, 0, 0, 1
    r, rp = a, b
    while rp != 0:
        q = r // rp
        r2, u2, v2 = r, u, v
        r, u, v = rp, up, vp
        rp, up, vp = r2 - q * r, u2 - q * up, v2 - q * vp
    assert a * u + b * v == gcd(a, b)
    return u, v

def existence_construction(c1: (int, int), c2: (int, int)) -> (int, int):
    a1, n1 = c1
    a2, n2 = c2
    m1, m2 = bezout(n1, n2)
    b = n1 * n2
    return (a1 * m2 * n2 + a2 * m1 * n1) % b, b

def contest(busses: [(int, int)]) -> int:
    return reduce(existence_construction, busses)[0]

with open(argv[1]) as fp:
    earliest = int(fp.readline().strip())
    busses = [(((v := int(id)) - i) % v, v) for i, id in enumerate(fp.readline().strip().split(',')) if id != 'x']

print(first_departure(earliest, [b for _, b in busses]))
print(contest(busses))
