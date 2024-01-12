from sys import argv
from math import sqrt
from collections import Counter
from functools import reduce
from operator import mul

try:
    n = int(argv[1])
except:
    with open('input.txt') as fp:
        text = fp.read()
    n = int(text.strip())

# i'th house gets 10 * sum(factors)

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
    return pf, reduce(mul, (p(b, e) for b, e in pf.items()), 1)

root = int(sqrt(n))
print('sqrt', root)
primes = primes_up_to(root)
print(len(primes), 'primes <', root)
print('sum of factors of', n, 'is', sum_of_factors(n))

i = 1
while True:
    pf, s = sum_of_factors(i)
    if s >= n//10:
        print(i, s, pf)
        break
    i += 1
