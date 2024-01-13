from sys import argv
from math import sqrt, prod
from collections import Counter
from functools import reduce
from operator import mul
from itertools import product

try:
    n = int(argv[1])
except:
    with open('input.txt') as fp:
        text = fp.read()
    n = int(text.strip())

def primes_up_to(n: int) -> [int]:
    cands = [True] * (n+1)
    cands[0] = False
    cands[1] = False
    primes = []
    for i in range(2, n+1):
        if cands[i]:
            primes.append(i)
            sq = i * i
            if sq <= n:
                for j in range(sq, n+1, i):
                    cands[j] = False
    return primes

def prime_factorization(n: int) -> {int: int}:
    factors = []
    for prime in primes:
        if prime * prime > n:
            break
        while n % prime == 0:
            factors.append(prime)
            n //= prime
    if n > 1:
        factors.append(n)
    return Counter(factors)

def sum_of_factors(n: int):
    pf = prime_factorization(n)
    def p(base: int, exp: int) -> int:
        return sum(base**i for i in range(exp+1))
    return pf, prod(p(b, e) for b, e in pf.items())

root = int(sqrt(n))
print('sqrt of', n, 'is', root)
primes = primes_up_to(root)
print('there are', len(primes), 'primes <', root)

def part1() -> int:
    i = 1
    while True:
        pf, s = sum_of_factors(i)
        if s >= n//10:
            print('house', i, 'gifts', 10*s, pf)
            return i
        i += 1

def integer_factorization(n: int) -> [int]:
    pf = prime_factorization(n)
    powers = [[base ** e for e in range(exp+1)] for base, exp in pf.items()]
    return sorted(set(prod(combo) for combo in product(*powers)))

def sum_of_contributing_factors(n: int, delta: int) -> int:
    factors = integer_factorization(n)
    return sum(factor for factor in factors if (factor * delta) >= n)

def part2() -> int:
    i = 1
    while True:
        s = sum_of_contributing_factors(i, 50)
        if s >= n//11:
            print('house', i, 'gifts', 11*s)
            return i
        i += 1

print(part1())
print(part2())
